import aiohttp
import asyncio

from loguru import logger

from goopy_misc.watchdog import Watchdog
from goopy_ibcp.error import Error
from goopy_ibcp.resultrequest import RequestResult


class HttpEndpointsAio(Watchdog):
    # TODO: Document HttpEndpointsAio class
    """
    HttpEndpoints
    Use async io to provide Get/Post operations for a base URL with endpoints.
    """
    # used for JSON GET/POST requests
    headers = {'accept': 'application/json'}

    def __init__(self, name='Unknown', timeout_sec=5, watchdog_start=True, disable_request_warnings=True):
        # kick off the watchdog
        super().__init__(name=name, timeout_sec=timeout_sec, autostart=watchdog_start)

        # gateway base URL for submitting all client portal API. All commands append to this string
        self.url_http = ''
        self.request_timeout_sec = 30

        # Statistic tracking
        self.count_timeouts = 0
        self.count_packets = 0
        self.count_exceptions = 0

        if disable_request_warnings:
            pass

    async def clientrequest_get(self, endpoint='', params=None):
        """ Gateway Get message request using desired endpoint. """
        result = await self.__request(method='GET', endpoint=endpoint, params=params)
        return result

    async def clientrequest_post(self, endpoint='', params=None):
        """ Gateway Post message request using desired endpoint."""
        result = await self.__request(method='POST', endpoint=endpoint, params=params)
        return result

    def __build_endpoint_url(self, endpoint: str = ''):
        url = self.url_http + endpoint
        return url

    @logger.catch
    async def __request(self, method:str='GET', endpoint:str='', params=None ):
        result = RequestResult()
        result.url = self.__build_endpoint_url(endpoint)

        logger.log('DEBUG', f'{method}-REQUEST({endpoint}), params={params}')

        # Without ssl=False, we get issues with untrusted SSL certificates
        # This should be ok for demo accounts and testing, but we should look in to proper SSL for live accounts
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method=method, url=result.url, ssl=False, timeout=self.request_timeout_sec, params=params) as response:
                    result.json = await response.json(content_type=None)
                    self.count_packets = self.count_packets + 1
                    logger.log('DEBUG', f'RESPONSE ({response.status}): {result.json}')
                    logger.log('DEBUG', f'Statistics: Packets={self.count_packets}, Timeouts={self.count_timeouts}, Exceptions={self.count_exceptions}')

        except asyncio.exceptions.TimeoutError as e:
            logger.log('DEBUG', f'Timeout: {method} after {self.request_timeout_sec}')
            self.count_timeouts = self.count_timeouts + 1 

        # Any exceptions and return will be passed off to __error_check for handling
        except Exception as e:
            self.count_exceptions = self.count_exceptions + 1
            logger.log('DEBUG', f'EXCEPTION: {e}')

        return result

if __name__ == '__main__':
    print("=== HTTP Endpoint ===")
