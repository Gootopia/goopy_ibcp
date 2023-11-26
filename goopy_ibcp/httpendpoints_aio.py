from json import JSONDecodeError
import aiohttp
import asyncio
import json
import xmltodict

from loguru import logger

# from goopy_misc.watchdog import Watchdog
from watchdog import Watchdog
from error import IBClientError
from resultrequest import RequestResult


class HttpEndpointsAio(Watchdog):
    # TODO: Document HttpEndpointsAio class
    """
    HttpEndpoints
    Use async io to provide Get/Post operations for a base URL with endpoints.
    """
    # used for JSON GET/POST requests
    # NOTE: 403 errors were being received until headers was modified per this page:
    # https://stackoverflow.com/questions/65305153/403-response-code-for-any-post-request-to-interactive-brokers-client-portal-web
    # headers = {"accept": "application/json"}
    headers = {"User-Agent": "Console", "content-type": "application/json"}

    def __init__(
        self,
        name="Unknown",
        timeout_sec=5,
        watchdog_start=True,
        disable_request_warnings=True,
    ):
        # kick off the watchdog
        super().__init__(name=name, timeout_sec=timeout_sec, autostart=watchdog_start)

        # gateway base URL for submitting all client portal API. All commands append to this string
        self.url_http = ""
        self.request_timeout_sec = 30

        # Statistic tracking
        self.count_timeouts = 0
        self.count_packets = 0
        self.count_exceptions = 0

        if disable_request_warnings:
            pass

    async def clientrequest_get(self, endpoint="", params=None, is_ib_endpoint=True):
        """Gateway Get message request using desired endpoint.
        If we want to use something other than IB Client URL, set is_ib_endpoint to False and provide the
        desired URL in the endpoint parameter
        """
        result = await self.__request(
            method="GET",
            endpoint=endpoint,
            params=params,
            is_ib_endpoint=is_ib_endpoint,
        )
        return result

    async def clientrequest_post(self, endpoint="", params=None):
        """Gateway Post message request using desired endpoint."""
        result = await self.__request(method="POST", endpoint=endpoint, params=params)
        return result

    def __build_endpoint_url(self, endpoint: str = ""):
        url = self.url_http + endpoint
        return url

    @logger.catch
    async def __request(
        self, method: str = "GET", endpoint: str = "", params=None, is_ib_endpoint=True
    ):
        result = RequestResult()

        # Normally, URL are IB client endpoints but for FlexQueries (or any other non-IB URL),
        # we use whatever the user provides in the endpoint string as the full URL
        if is_ib_endpoint is True:
            result.url = self.__build_endpoint_url(endpoint)
        else:
            result.url = endpoint

        logger.log("DEBUG", f"{method}-REQUEST({endpoint}), params={params}")

        # Without ssl=False, we get issues with untrusted SSL certificates
        # This should be ok for demo accounts and testing, but we should look in to proper SSL for live accounts
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=result.url,
                    headers=HttpEndpointsAio.headers,
                    ssl=False,
                    timeout=self.request_timeout_sec,
                    # params=params,
                    json=params,
                ) as response:
                    # Save the raw string in case we need it.
                    result.raw = await response.text()

                    # Flex Queries can return a variety of content. Will expand as we get different types
                    # For now, it's best to select "XML" as the data type when creating the Flex Query
                    if response.content_type == "text/xml":
                        result.dict = xmltodict.parse(result.raw)
                        result.json = json.dumps(result.dict)
                    elif response.content_type == "text/plain":
                        pass
                    else:
                        result.json = await response.json(content_type=None)

                    # Packet counter just for info purposes
                    self.count_packets = self.count_packets + 1

                    # Check returns. 200=good. Others indicate errors
                    if response.status == 200:
                        result.error = IBClientError.Err_General_Ok

                    elif response.status == 401:
                        result.error = (
                            IBClientError.Err_Connection_Incomplete_WebRequest_401
                        )

                    elif response.status == 403:
                        result.error = (
                            IBClientError.Err_Connection_Unauthorized_Web_Request_403
                        )

                    else:
                        result.error = IBClientError.Err_Connection_Unhandled_Web_Error
                    logger.log("DEBUG", f"RESPONSE ({response.status}): {result.json}")
                    logger.log(
                        "DEBUG",
                        f"Statistics: Packets={self.count_packets}, Timeouts={self.count_timeouts}, Exceptions={self.count_exceptions}",
                    )

        except JSONDecodeError as e:
            logger.log(
                "DEBUG",
                f"JSONDecode: Status={response.status}, Reason={response.reason}, Body={response._body}",
            )
            self.count_exceptions = self.count_exceptions + 1

        except asyncio.exceptions.TimeoutError as e:
            logger.log("DEBUG", f"Timeout: {method} after {self.request_timeout_sec}")
            self.count_timeouts = self.count_timeouts + 1

        # Can't talk to the ClientPortal gateway. May not be running?
        except aiohttp.ClientConnectionError as e:
            logger.log(
                "DEBUG", f"Can't connect to ClientPortal. Verify Gateway is running!"
            )
            result.error = IBClientError.Err_Connection_No_Gateway

        # Log all received exceptions. We may handle other specific ones as they arise
        except Exception as e:
            self.count_exceptions = self.count_exceptions + 1
            logger.log("DEBUG", f"EXCEPTION: {e}")

        return result


if __name__ == "__main__":
    print("=== HTTP Endpoint ===")
