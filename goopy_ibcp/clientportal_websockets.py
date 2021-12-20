import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from loguru import logger
import json

from goopy_certificate.certificate import Certificate, CertificateError

class ClientPortalWebsocketsError(Enum):
    Ok = 0
    Unknown = 1
    Invalid_URL = 2
    Invalid_Certificate = 3
    Connection_Failed = 4


# TODO: Document ClientPortalWebsocketsBase class
class ClientPortalWebsocketsBase:
    """
    Interactive Brokers ClientPortal Interface (Websocket).
    Refer to https://interactivebrokers.github.io/cpwebapi/RealtimeSubscription.html for API documentation
    NOTE: Websocket usage also requires the UI to send the /tickle endpoint. See Websocket Ping Session docs.
    """
    def __init__(self):
        # Base used by all IB websocket endpoints
        self.url_ib_wss = 'wss://localhost:5000/v1/api/ws'
        self.connection = None
        self.sslcontext = None
        # default websocket 'tic' heartbeat message is 60 sec
        self.heartbeat_sec = 60
        self.data_subscribers = []
        logger.log('DEBUG', f'Clientportal (Websockets) Started with endpoint: {self.url_ib_wss}')
        
    def loop(self):
        """ Start websocket message handler and heartbeat """
        try:
            with ThreadPoolExecutor() as executor:
                executor.submit(asyncio.get_event_loop().run_until_complete(self.__async_loop()))

        except Exception as e:
            logger.log('DEBUG', f'Exception:{e}')

        finally:
            pass

    def on_connection(self, msg):
        """ Websocket connection opened. Override as required """
        pass

    def on_message(self, msg):
        """ Websocket message received. Override as required """
        pass

    async def __open_connection(self, url='', url_validator=None):
        """ Open a websocket connection """
        if url_validator is not None:
            if url_validator(url) is False:
                return ClientPortalWebsocketsError.Invalid_URL

        try:
            logger.log('DEBUG', f'Certificate: Acquiring')
            result = Certificate.get_certificate()

        except Exception as e:
            logger.log('DEBUG', f'EXCEPTION: {e}')
            return ClientPortalWebsocketsError.Unknown

        finally:
            if result.error != CertificateError.Ok:
                logger.log('DEBUG', f'Certificate: Problems obtaining certificate: {result.error}')
                return ClientPortalWebsocketsError.Invalid_Certificate

        try:
            logger.log('DEBUG', f'Connection: Opening "{url}"')

            self.connection = await websockets.connect(url, ssl=result.ssl_context)
            logger.log('DEBUG', f'Connection: Established "{url}"')
            ret_code = ClientPortalWebsocketsError.Ok

            # Once connection is achieved, IB provides confirmation message with username
            connect_msg = await self.connection.recv()
            logger.log('DEBUG', f'Connection: Confirmation {connect_msg}')

            # additional external handling if overridden
            self.on_connection(connect_msg)

            # save off this context for use by other handlers since it was used successfully already
            self.sslcontext = result.ssl_context

        except websockets.WebSocketException as e:
            logger.log('DEBUG', f'EXCEPTION: Websockets {e}')
            ret_code = ClientPortalWebsocketsError.Connection_Failed

        except Exception as e:
            logger.log('DEBUG', f'EXCEPTION: General exception: {e}')
            ret_code = ClientPortalWebsocketsError.Unknown

        finally:
            return ret_code

    async def __websocket_msg_handler(self):
        logger.log('DEBUG', f'Websocket: Start message handler')

        async for ws in websockets.connect(self.url_ib_wss, ssl=self.sslcontext):
            self.connection = ws
            if len(self.data_subscribers) > 0:
                logger.log('DEBUG', f'Websocket: Adding subscribers')
                for conid in self.data_subscribers:
                    subscriber_msg=f'smd+{conid}+{"fields":["31"]}'
                    await self.connection.send(subscriber_msg)
                    logger.log('DEBUG', f'Websocket: Subscribing to {conid}')

            try:
                async for msg in ws:
                    logger.log('DEBUG', f'Websocket: Received {msg}')
            
            except websockets.ConnectionClosed:
                logger.log('DEBUG', f'Websocket: Connection closed. Re-opening...')
                continue

            except Exception as e:
                logger.log('DEBUG', f'EXCEPTION: {e}')

            finally:
                pass

        logger.log('DEBUG', f'Websocket: Exited message handler. Restarting.')

    async def __websocket_heartbeat(self):
        if self.connection is not None:
            logger.log('DEBUG', f'Websocket: Start heartbeat')

            try:
                while True:
                    await self.connection.send('tic')
                    logger.log('DEBUG', f'Websocket: Heartbeat {self.heartbeat_sec}s')
                    await asyncio.sleep(self.heartbeat_sec)

            except Exception as e:
                logger.log('DEBUG', f'EXCEPTION: {e}')

            finally:
                logger.log('DEBUG', f'Exited websocket heartbeat')

    async def __websocket_reqdata(self):
        await asyncio.sleep(15)
        logger.log('DEBUG', f'Requesting Data!')
        await self.connection.send('smd+461318816+{"fields":["31"]}')
        logger.log('DEBUG', f'Exiting ReqData')

    async def __async_loop(self):
        try:
            ret = await self.__open_connection(url=self.url_ib_wss)
            if ret == ClientPortalWebsocketsError.Ok:
                await asyncio.gather(self.__websocket_msg_handler(), self.__websocket_reqdata())

        except Exception as e:
            logger.log('DEBUG', f'EXCEPTION: {e}')

        finally:
            logger.log('DEBUG', f'Websocket: Exited loop')


if __name__ == '__main__':
    print("=== IB Client Portal Websockets ===")