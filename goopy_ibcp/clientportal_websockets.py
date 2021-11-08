import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pathlib import Path

from loguru import logger

from goopy_certificate import Certificate, CertificateError


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
        self.url = 'wss://localhost:5000/v1/api/ws'
        self.connection = None
        # default websocket 'tic' heartbeat message is 60 sec
        self.heartbeat_sec = 60
        logger.log('DEBUG', f'Clientportal (Websockets) Started with endpoint: {self.url}')

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
        """ Websocket connection opened """
        pass

    def on_message(self, msg):
        """ Websocket message received """
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
            logger.log('DEBUG', f'Connection: Opening "{self.url}"')
            self.connection = await websockets.connect(self.url, ssl=result.ssl_context)
            logger.log('DEBUG', f'Connection: Established "{self.url}"')
            ret_code = ClientPortalWebsocketsError.Ok

            # Once connection is achieved, IB provides confirmation message with username
            connect_msg = await self.connection.recv()
            logger.log('DEBUG', f'Connection: Confirmation {connect_msg}')
            self.on_connection(connect_msg)

        except websockets.WebSocketException as e:
            logger.log('DEBUG', f'EXCEPTION: Websockets {e}')
            ret_code = ClientPortalWebsocketsError.Connection_Failed

        except Exception as e:
            logger.log('DEBUG', f'EXCEPTION: General exception: {e}')
            ret_code = ClientPortalWebsocketsError.Unknown

        finally:
            return ret_code

    async def __websocket_msg_handler(self):
        if self.connection is not None:
            logger.log('DEBUG', f'Websocket: Start message handler')
            try:
                while True:
                    msg = await self.connection.recv()
                    logger.log('DEBUG', f'Websocket: Received {msg}')

            except Exception as e:
                logger.log('DEBUG', f'EXCEPTION: {e}')

            finally:
                logger.log('DEBUG', f'Websocket: Exited message handler')

        else:
            logger.log('DEBUG', f'Websocket: Handler has no valid connection')

    async def __websocket_heartbeat(self):
        if self.connection is not None:
            logger.log('DEBUG', f'Websocket: Start heartbeat')

            try:
                while True:
                    await self.connection.send('tic')
                    await asyncio.sleep(self.heartbeat_sec)

            except Exception as e:
                logger.log('DEBUG', f'EXCEPTION: {e}')

            finally:
                logger.log('DEBUG', f'Exited websocket heartbeat')

    async def __async_loop(self):
        try:
            task_connection = asyncio.create_task(self.__open_connection())
            # msg_handler and heartbeat depend on opening a valid connection
            ret = await task_connection
            if ret == ClientPortalWebsocketsError.Ok:
                status = await asyncio.gather(self.__websocket_msg_handler(), self.__websocket_heartbeat())

        except Exception as e:
            logger.log('DEBUG', f'EXCEPTION: {e}')

        finally:
            logger.log('DEBUG', f'Websocket: Exited loop')


if __name__ == '__main__':
    print("=== IB Client Portal Websockets ===")