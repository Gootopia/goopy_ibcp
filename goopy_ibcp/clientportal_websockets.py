import asyncio
import subprocess
import sys
import websockets
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from loguru import logger

from zmq_publisher import ZmqPublisher

# from goopy_certificate.certificate import Certificate, CertificateError
from ibfieldmapper import IBFieldMapper
from certificate import Certificate, CertificateError
from ibmsg_tick import IBMsgConverterTick
from ibmsg import IBMsgConverter
from jsonpacket import JSONPacket
from ibmsg_topic import IBTopic
from error import IBClientError


class ClientPortalWebsocketConnectionStatus(Enum):
    Not_Connected = 1
    Waiting_For_Connection = 2
    Connected = 3


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
        self.connection_state = ClientPortalWebsocketConnectionStatus.Not_Connected
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
            return IBClientError.Err_MarketData_Conid_Invalid

        topic = f"smd+{conid}"
        fields = '{"fields":}' + str(f"{ticks}")
        ticks = ",".join([f'"{str(tick)}"' for tick in ticks])
        smd_string = f'{topic}+{{"fields":[{ticks}]}}'
        return IBClientError.Err_General_Ok, smd_string

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
        logger.log("DEBUG", f"Entered websocket loop")
        try:
            with ThreadPoolExecutor() as executor:
                executor.submit(
                    # asyncio.get_event_loop().run_until_complete(self.__async_loop()),
                    asyncio.run(self.__async_loop())
                )

        except Exception as e:
            logger.log("DEBUG", f"Exception:{e}")

        finally:
            logger.log("DEBUG", f"Exited websocket loop.")

    async def send(self, msg):
        """Websocket send. Automatic logging of transmitted data."""
        if self.connection is not None:
            logger.log("DEBUG", f"{msg}")
            await self.connection.send(msg)

    def on_connection(self):
        """Websocket connection opened. Override as required."""
        pass

    def on_message(self, msg):
        """Websocket message received. Override as required."""
        pass

    def subscribe_data(self, conid: str, ticks: list = [IBFieldMapper.Price_Last]):
        """Subscribe to streaming websocket data for desired contract id
        Return only desired ticks:
        {conid} = Contract ID (see https://pennies.interactivebrokers.com/cstools/contract_info/v3.10/index.php)
        {ticks} = List of desired ticks (See IBFieldmapper)"""
        valid_ticks = ClientPortalWebsocketsBase._check_tick_types(ticks)

        # User is responsible for making sure conid is valid but we'll do rudimentary check on format
        if conid.isdigit is False:
            return IBClientError.Err_MarketData_Conid_Not_Integer

        if valid_ticks:
            ws_str = ClientPortalWebsocketsBase._build_ws_str_smd(conid, valid_ticks)
            ws_str = ws_str

    async def __open_connection(
        self,
        url="",
        url_validator=None,
        connection_max_attempts: int = 0,
        retry_timeout_sec: int = 15,
    ):
        """Open a websocket connection
        {url} = self explanatory
        {url_validator} = method that can be used to check/coerce URL that is passed
        {num_retries} = Number of retry attempts if connection fails (0 for infinite)
        {retry_timeout_sec} = Seconds to wait between retries"""
        if url_validator is not None:
            if url_validator(url) is False:
                return IBClientError.Err_General_Invalid_URL

        try:
            logger.log("DEBUG", f"Acquiring certificate.")
            result = Certificate.get_certificate()

        except Exception as e:
            logger.log("DEBUG", f"EXCEPTION: {e}")
            return IBClientError.Err_Websocket_Unhandled_Exception

        finally:
            if result.error != CertificateError.Ok:
                logger.log(
                    "DEBUG",
                    f"Problems obtaining certificate: {result.error}",
                )
                return IBClientError.Err_Websocket_Invalid_Certificate

        connection_attempts = 1

        while connection_attempts > connection_max_attempts:
            try:
                logger.log("DEBUG", f"Attempting connection to {url}")
                self.connection = await websockets.connect(url, ssl=result.ssl_context)

                self.connection_state = ClientPortalWebsocketConnectionStatus.Connected

                # Once connection is achieved, IB provides confirmation message with username
                # connect_msg = await self.connection.recv()
                # logger.log("DEBUG", f"Received: {connect_msg}")

                # additional external handling if overridden
                # self.on_connection(connect_msg)

                # save off this context for use by other handlers since it was used successfully already
                self.sslcontext = result.ssl_context

                # We can only get here if the connection succeeds, otherwise we process the resulting exception
                logger.log("DEBUG", f"Connected to {url}.")
                ret_val = IBClientError.Err_General_Ok

            except (websockets.WebSocketException, TimeoutError) as e:
                logger.log("DEBUG", f"EXCEPTION: Websockets {e}")
                ret_val = IBClientError.Err_Websocket_Connection_Failed

            except ConnectionRefusedError as e:
                logger.log("DEBUG", f"EXCEPTION: Connection refused. Retrying {e}")
                ret_val = IBClientError.Err_Websocket_Connection_Refused

            except Exception as e:
                logger.log("DEBUG", f"EXCEPTION: General exception: {e}")
                ret_val = IBClientError.Err_Websocket_Unhandled_Exception

            finally:
                # On anything other than good connection, we retry until success or max attempts
                if ret_val == IBClientError.Err_General_Ok:
                    break
                else:
                    self.connection_state = (
                        ClientPortalWebsocketConnectionStatus.Not_Connected
                    )

                    connection_attempts = connection_attempts + 1
                    logger.log(
                        "DEBUG",
                        f"Connection attempt {connection_attempts} failed. Retry in {retry_timeout_sec}s.",
                    )
                    await asyncio.sleep(retry_timeout_sec)

        # Return after maximum attempts
        return ret_val

    async def __websocket_msg_handler(self):
        """Process incoming IB messages. Will publish via ZMQ as appropriate (see init)"""
        logger.log("DEBUG", f"Starting message handler")

        async for ws in websockets.connect(self.url_ib_wss, ssl=self.sslcontext):
            try:
                self.connection = ws

                async for msg_raw in ws:
                    logger.log("DEBUG", f"Received from IB: {msg_raw}")

                    # Don't know what message type is yet
                    new_msg_dict = IBMsgConverter.create_dict_from_raw_msg(msg_raw)

                    # IB delivers most messages as "topic" with a sub-field
                    found_topic = IBTopic.Topic in new_msg_dict.keys()
                    found_message = IBTopic.Message in new_msg_dict.keys()

                    if found_topic == True:
                        new_msg_topic = new_msg_dict[IBTopic.Topic]

                        # If a handler is available, we'll get a specific message dictionary returned to us
                        handled_msg_dict = IBTopic.process_topic(
                            new_msg_topic, self.msg_handlers, msg_raw
                        )

                        # Only publish packets to ZMQ that have been configured to do so (see class init)
                        if handled_msg_dict is not None:
                            new_json_packet = JSONPacket(
                                new_msg_topic, handled_msg_dict
                            )
                            xmit_msg = new_json_packet.build_packet()
                            self.publisher.publish_string(xmit_msg)
                            logger.log("DEBUG", f"ZMQ Tx: {xmit_msg}")

                    # This doesn't appear to be documented, but normally shows up while waiting for connection
                    elif found_message == True and found_topic == False:
                        new_msg: str = new_msg_dict[IBTopic.Message]
                        logger.log("DEBUG", f"Non-topic message: '{new_msg}'")

                        found_msg = new_msg.find("waiting for session")
                        # It is expected that we receive the "waiting for session". If so, ignore
                        if found_msg == 0:
                            pass

                        else:
                            logger.log(
                                "DEBUG", f"Unknown message received: '{new_msg}'"
                            )

            except websockets.ConnectionClosed:
                logger.log("DEBUG", f"Connection closed.")
                ret_val = IBClientError.Err_Websocket_Connection_Closed

            except KeyError as e:
                logger.log("DEBUG", f"Missing Key: {e}")
                ret_val = IBClientError.Err_Websocket_Missing_Key

            except Exception as e:
                logger.log("DEBUG", f"EXCEPTION: {e}")
                ret_val = IBClientError.Err_Websocket_Unhandled_Exception

            finally:
                if ret_val != IBClientError.Err_General_Ok:
                    self.connection_state = (
                        ClientPortalWebsocketConnectionStatus.Not_Connected
                    )

                logger.log("DEBUG", f"Exited message handler.")

            return ret_val

    async def __websocket_heartbeat(self):
        if self.connection is not None:
            logger.log("DEBUG", f"Start heartbeat every {self.heartbeat_sec}")

            try:
                while True:
                    await self.send("tic")

                    logger.log("DEBUG", f"Send Heartbeat {self.heartbeat_sec}s")
                    await asyncio.sleep(self.heartbeat_sec)

            except websockets.ConnectionClosedError:
                logger.log("DEBUG", f"Connection closed.")
                ret_val = IBClientError.Err_Websocket_Connection_Closed

            except Exception as e:
                logger.log("DEBUG", f"EXCEPTION: {e}")
                ret_val = IBClientError.Err_Websocket_Unhandled_Exception

            finally:
                if ret_val != IBClientError.Err_General_Ok:
                    self.connection_state = (
                        ClientPortalWebsocketConnectionStatus.Not_Connected
                    )

                logger.log("DEBUG", f"Exited websocket heartbeat")

            return ret_val

    async def __websocket_reqdata_example(self):
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
        ticks = [IBFieldMapper.Price_Last]

        # Example request just to get a tick stream started
        result, ws_str = self._build_ws_str_smd(conid, ticks)
        if result == IBClientError.Err_General_Ok:
            await self.send(ws_str)
            logger.log("DEBUG", f"Sent streaming data request")
        else:
            logger.log("DEBUG", f"Websocket string error: {result}")

        # Example request to initiate historical data gathering
        # await self.send(
        #    'smh+586139726+{"period": "1d","bar": "1min", "source": "trades","format": "%c", "outsideRth":true, "since":"20230510-22:00:00}'
        # )
        # logger.log("DEBUG", f"Sent historical data request")
        logger.log("DEBUG", f"Exit ReqData")

    async def __async_loop(self, restart_async_loop: bool = True):
        """Asyncio loop to handle heartbeat, and messages from IB client.
        {restart_async_loop} = Restart loop if connection is closed."""
        # Start the infinite thread loop
        # If we exit the loop for some reason, these will be returned to caller
        asyncio_gather_results = None

        while restart_async_loop == True:
            try:
                logger.log("DEBUG", f"Starting Asyncio Loop")

                ret_val = await self.__open_connection(url=self.url_ib_wss)

                if ret_val == IBClientError.Err_General_Ok:
                    # Base method loops we always need
                    methods = [
                        self.__websocket_msg_handler(),
                        self.__websocket_heartbeat(),
                    ]

                    # Can append additional methods as needed
                    methods.append(self.__websocket_reqdata_example())

                    # pass in desired list as arguments
                    asyncio_gather_results = await asyncio.gather(*methods)

                    if (
                        IBClientError.Err_Websocket_Connection_Closed
                        in asyncio_gather_results
                    ):
                        logger.log("DEBUG", "Connection closed. Restarting.")

            except Exception as e:
                logger.log("DEBUG", f"EXCEPTION: {e}")
                # TODO: Identify any exceptions that get here. Until then, exit without restart
                restart_async_loop = False

            finally:
                if restart_async_loop != True:
                    logger.log("DEBUG", f"Exited Async Loop")


@logger.catch
def main_ws() -> None:
    logger.add("testlog.log")

    client_ws = ClientPortalWebsocketsBase()
    client_ws.loop()


if __name__ == "__main__":
    # Example to start an infinite event loop which handles websocket messages
    # Refer to _async_loop for more details on specific threads
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main_ws())
    asyncio.run(main_ws())
