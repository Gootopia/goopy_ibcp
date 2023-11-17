import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from loguru import logger

from goopy_ibcp.zmq_publisher import ZmqPublisher

# from goopy_certificate.certificate import Certificate, CertificateError
from goopy_ibcp.ibfieldmapper import IBFieldMapper
from goopy_ibcp.certificate import Certificate, CertificateError
from goopy_ibcp.ibmsg_tick import IBMsgConverterTick
from goopy_ibcp.ibmsg import IBMsgConverter
from goopy_ibcp.jsonpacket import JSONPacket
from goopy_ibcp.ibmsg_topic import IBTopic


class ClientPortalWebsocketsError(Enum):
    """Define client portal error messages."""

    Ok = 0
    Unknown = 1
    Invalid_URL = 2
    Invalid_Certificate = 3
    Connection_Failed = 4
    Invalid_Conid = 5


# TODO: Document ClientPortalWebsocketsBase class
class ClientPortalWebsocketsBase:
    """
    Interactive Brokers ClientPortal Interface (Websocket).
    Refer to https://interactivebrokers.github.io/cpwebapi/RealtimeSubscription.html for API documentation
    NOTE: Websocket usage also requires the UI to send the /tickle endpoint. See Websocket Ping Session docs.
    """

    def __init__(self):
        # Base used by all IB websocket endpoints
        self.url_ib_wss = "wss://localhost:5000/v1/api/ws"
        self.connection = None
        self.sslcontext = None
        self.msg_handlers = {}
        # default websocket 'tic' heartbeat message is 60 sec
        self.heartbeat_sec = 60
        self.data_subscribers = []
        self.publisher = ZmqPublisher()
        logger.log(
            "DEBUG",
            f"Clientportal (Websockets) Started with endpoint: {self.url_ib_wss}",
        )

        # Message converters we want to handle. Other messages will be discarded when received.
        self.msg_handlers[
            IBTopic.MarketData
        ] = IBMsgConverterTick.create_dict_from_raw_msg

    @staticmethod
    def _build_ws_str_smd(conid: str, ticks: list) -> str:
        """Helper string to build up subscriptionstrings IB websocket understands
        Refer to: https://interactivebrokers.github.io/cpwebapi/websockets for formats
        """
        # conid are always an integer
        if conid.isdigit() is False:
            return ClientPortalWebsocketsError.Invalid_Conid

        topic = f"smd+{conid}"
        fields = '{"fields":}' + str(f"{ticks}")
        ticks = ",".join([f'"{str(tick)}"' for tick in ticks])
        smd_string = f'{topic}+{{"fields":[{ticks}]}}'
        return ClientPortalWebsocketsError.Ok, smd_string

    @staticmethod
    def _check_tick_types(ticks_requested: list) -> list:
        """Helper function to only pass valid tick types."""
        ticks_used = []

        if IBFieldMapper.Price_Ask in ticks_requested:
            ticks_used.append(IBFieldMapper.Price_Ask)

        if IBFieldMapper.Price_Bid in ticks_requested:
            ticks_used.append(IBFieldMapper.Price_Bid)

        if IBFieldMapper.Price_Close in ticks_requested:
            ticks_used.append(IBFieldMapper.Price_Close)

        if IBFieldMapper.Price_High in ticks_requested:
            ticks_used.append(IBFieldMapper.Price_High)

        if IBFieldMapper.Price_Last in ticks_requested:
            ticks_used.append(IBFieldMapper.Price_Last)

        if IBFieldMapper.Price_Low in ticks_requested:
            ticks_used.append(IBFieldMapper.Price_Low)

        if IBFieldMapper.Price_Open in ticks_requested:
            ticks_used.append(IBFieldMapper.Price_Open)

        return ticks_used

    def loop(self):
        """Start websocket message handler and heartbeat"""
        try:
            with ThreadPoolExecutor() as executor:
                executor.submit(
                    asyncio.get_event_loop().run_until_complete(self.__async_loop())
                )

        except Exception as e:
            logger.log("DEBUG", f"Exception:{e}")

        finally:
            logger.log("DEBUG", f"Exited loop.")

    async def send(self, msg):
        """Websocket send. Automatic logging of transmitted data."""
        if self.connection is not None:
            logger.log("DEBUG", f"{msg}")
            await self.connection.send(msg)

    def on_connection(self, msg):
        """Websocket connection opened. Override as required."""
        pass

    def on_message(self, msg):
        """Websocket message received. Override as required."""
        pass

    async def __open_connection(self, url="", url_validator=None):
        """Open a websocket connection"""
        if url_validator is not None:
            if url_validator(url) is False:
                return ClientPortalWebsocketsError.Invalid_URL

        try:
            logger.log("DEBUG", f"Certificate: Acquiring")
            result = Certificate.get_certificate()

        except Exception as e:
            logger.log("DEBUG", f"EXCEPTION: {e}")
            return ClientPortalWebsocketsError.Unknown

        finally:
            if result.error != CertificateError.Ok:
                logger.log(
                    "DEBUG",
                    f"Certificate: Problems obtaining certificate: {result.error}",
                )
                return ClientPortalWebsocketsError.Invalid_Certificate

        try:
            logger.log("DEBUG", f'Connection: Opening "{url}"')

            self.connection = await websockets.connect(url, ssl=result.ssl_context)
            logger.log("DEBUG", f'Connection: Established "{url}"')
            ret_code = ClientPortalWebsocketsError.Ok

            # Once connection is achieved, IB provides confirmation message with username
            connect_msg = await self.connection.recv()
            logger.log("DEBUG", f"Connection: Confirmation {connect_msg}")

            # additional external handling if overridden
            self.on_connection(connect_msg)

            # save off this context for use by other handlers since it was used successfully already
            self.sslcontext = result.ssl_context

        except (websockets.WebSocketException, TimeoutError) as e:
            logger.log("DEBUG", f"EXCEPTION: Websockets {e}")
            ret_code = ClientPortalWebsocketsError.Connection_Failed

        except Exception as e:
            logger.log("DEBUG", f"EXCEPTION: General exception: {e}")
            ret_code = ClientPortalWebsocketsError.Unknown

        finally:
            return ret_code

    async def __websocket_msg_handler(self):
        logger.log("DEBUG", f"Start message handler")

        async for ws in websockets.connect(self.url_ib_wss, ssl=self.sslcontext):
            try:
                self.connection = ws

                async for msg_raw in ws:
                    logger.log("DEBUG", f"Received {msg_raw}")

                    # Don't know what message type is yet, so just use base and extract the topic
                    new_msg_dict = IBMsgConverter.create_dict_from_raw_msg(msg_raw)
                    new_msg_topic = new_msg_dict[IBTopic.Topic]

                    # If a handler is available, we'll get a specific message dictionary returned to us
                    handled_msg_dict = IBTopic.process_topic(
                        new_msg_topic, self.msg_handlers, msg_raw
                    )

                    # Only transmit packets that were handled
                    if handled_msg_dict is not None:
                        new_json_packet = JSONPacket(new_msg_topic, handled_msg_dict)
                        xmit_msg = new_json_packet.build_packet()
                        self.publisher.publish_string(xmit_msg)
                        logger.log("DEBUG", f"Transmitted: {xmit_msg}")

            except websockets.ConnectionClosed:
                logger.log("DEBUG", f"Connection closed. Re-opening...")
                continue

            except Exception as e:
                logger.log("DEBUG", f"EXCEPTION: {e}")

            finally:
                pass

        logger.log("DEBUG", f"Exited message handler. Restarting.")

    async def __websocket_heartbeat(self):
        if self.connection is not None:
            logger.log("DEBUG", f"Start heartbeat")

            try:
                while True:
                    await self.send("tic")

                    logger.log("DEBUG", f"Send Heartbeat {self.heartbeat_sec}s")
                    await asyncio.sleep(self.heartbeat_sec)

            except Exception as e:
                logger.log("DEBUG", f"EXCEPTION: {e}")

            finally:
                logger.log("DEBUG", f"Exited websocket heartbeat")

    async def __websocket_reqdata(self):
        # Subscribe to desired data feeds.
        # Short sleep to let things get connected...TBD needed? Better way?
        await asyncio.sleep(5)
        logger.log("DEBUG", f"Start ReqData")

        # Contract ID
        # MES, Dec 2023
        # Refer to https://misc.interactivebrokers.com/cstools/contract_info/v3.10/index.php?action=Conid
        # NOTE: If you are logged into the main account, the paper account will not transmit quote data
        # You can usually tell this if you subscribe and get one updated message but no quote data
        conid = "586139726"

        # Example request just to get a tick stream started
        topic = f"smd+{conid}"
        fields = f'{"fields":["31", "84", "86"]}'
        await self.send('smd+586139726+{"fields":["31", "84", "86"]}')
        logger.log("DEBUG", f"Sent streaming data request")

        # Example request to initiate historical data gathering
        # await self.send(
        #    'smh+586139726+{"period": "1d","bar": "1min", "source": "trades","format": "%c", "outsideRth":true, "since":"20230510-22:00:00}'
        # )
        logger.log("DEBUG", f"Sent historical data request")
        logger.log("DEBUG", f"Exit ReqData")

    async def __async_loop(self):
        # Kick off the various threads
        try:
            logger.log("DEBUG", f"Start Async Loop")
            ret = await self.__open_connection(url=self.url_ib_wss)
            if ret == ClientPortalWebsocketsError.Ok:
                await asyncio.gather(
                    self.__websocket_msg_handler(),
                    self.__websocket_reqdata(),
                    self.__websocket_heartbeat(),
                )
        except Exception as e:
            logger.log("DEBUG", f"EXCEPTION: {e}")

        finally:
            logger.log("DEBUG", f"Exited Async Loop")


@logger.catch
def main_ws() -> None:
    logger.add("testlog.log")

    client_ws = ClientPortalWebsocketsBase()
    client_ws.loop()


if __name__ == "__main__":
    # Example to start an infinite event loop which handles websocket messages
    # Refer to _async_loop for more details on specific threads
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_ws())
