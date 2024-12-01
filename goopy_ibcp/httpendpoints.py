""" DEPRECATED. Use httpendpoints_aio.py!"""

import requests
import urllib3

from loguru import logger

# from goopy_misc.watchdog import Watchdog
from watchdog import Watchdog
from error import IBClientError
from resultrequest import RequestResult


class HttpEndpoints(Watchdog):
    # TODO: Document HttpEndpoints class
    """
    HttpEndpoints
    Provide Get/Post operations for a base URL with endpoints.
    """
    # used for JSON GET/POST requests
    # headers = {'accept': 'application/json'}
    headers = {
        "User-Agent": "Console",
        "content-type": "application/json",
        "accept": "application/json",
    }

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

        if disable_request_warnings:
            urllib3.disable_warnings()

    def clientrequest_get(self, endpoint="", params=None):
        """Gateway Get message request using desired endpoint."""
        cpurl, resp, exception = self.__get(endpoint, params=params)
        logger.log("DEBUG", f"GET({endpoint}), params={params}")
        result = self.__error_check(cpurl, resp, exception)
        logger.log(
            "DEBUG",
            f"GET-RESPONSE({endpoint}), status={result.statusCode}, error={result.error}, msg={result.json} ",
        )
        return result

    def clientrequest_post(self, endpoint="", params=None):
        """Gateway Post message request using desired endpoint."""
        cpurl, resp, exception = self.__post(endpoint, params=params)
        logger.log("DEBUG", f"POST({endpoint}), params={params}")
        result = self.__error_check(cpurl, resp, exception)
        logger.log(
            "DEBUG",
            f"POST-RESPONSE({endpoint}), status={result.statusCode}, error={result.error}, msg={result.json} ",
        )
        return result

    def __build_endpoint_url(self, endpoint: str = ""):
        url = self.url_http + endpoint
        return url

    def __get(self, endpoint: str = "", params=None):
        cpurl = self.__build_endpoint_url(endpoint)
        resp = None
        resp_exception = None
        # Without verify=False, we get issues with untrusted SSL certificates
        # This should be ok for demo accounts, but need to follow up on this for live accounts
        # See https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
        # resp is the web response. Use resp.json() to get the client request specific response
        # resp = requests.post(cpurl, headers=self.headers, json=data, verify=False)
        try:
            resp = requests.get(
                cpurl,
                headers=HttpEndpoints.headers,
                params=params,
                verify=False,
                timeout=self.request_timeout_sec,
            )

        except requests.Timeout:
            logger.log("DEBUG", f"Timeout: GET after {self.request_timeout_sec}")

        # Any exceptions and return will be passed off to __error_check for handling
        except Exception as e:
            resp_exception = e

        # TODO: Refactor to use dataclass
        return cpurl, resp, resp_exception

    def __post(self, endpoint: str = "", params=None):
        cpurl = self.__build_endpoint_url(endpoint)
        resp = None
        resp_exception = None

        # Without verify=False, we get issues with untrusted SSL certificates
        # This should be ok for demo accounts, but need to follow up on this for live accounts
        # See https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
        # resp is the web response. Use resp.json() to get the client request specific response
        try:
            resp = requests.post(
                cpurl,
                headers=HttpEndpoints.headers,
                params=params,
                verify=False,
                timeout=self.request_timeout_sec,
            )

        except requests.Timeout:
            logger.log("DEBUG", f"Timeout: GET after {self.request_timeout_sec}")

        # any exceptions will be passed off to __error_check for handling
        except Exception as e:
            resp_exception = e

        # TODO: Refactor to use dataclass
        return cpurl, resp, resp_exception

    @staticmethod
    def __error_check(cpurl, resp, exception):
        result = RequestResult()

        # resp will be None if we had an exception
        if resp is not None:
            # If Ok = False, there was a problem submitting the request, typically an invalid URL
            if not resp.ok:
                result.error = IBClientError.Err_General_Invalid_URL
            else:
                # conversion to give the request specific json results
                result.json = resp.json()
                result.statusCode = resp.status_code
        else:
            result.error = IBClientError.Connection_or_Timeout
            logger.log("DEBUG", f"{exception}")

        if result.error != IBClientError.Err_General_Ok:
            logger.log(
                "DEBUG", f"{cpurl}: Error={result.error}, Status={result.statusCode}"
            )

        return result


if __name__ == "__main__":
    print("=== HTTP Endpoint ===")
