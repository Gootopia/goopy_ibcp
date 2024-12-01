import os
from overrides import overrides
from loguru import logger


from goopy_ibcp.endpoints import Endpoints
from goopy_ibcp.error import IBClientError
from goopy_ibcp.httpendpoints_aio import HttpEndpointsAio
from goopy_ibcp.environment_var import Environment_Var
from goopy_ibcp.ibflexquery3 import IBFlexQuery3


class ClientPortalHttpAio(HttpEndpointsAio):
    # TODO: Document ClientPortalHttpAio class
    """
    Interactive Brokers ClientPortal Interface (HTTP).
    Refer to https://www.interactivebrokers.com/api/doc.html for API documentation
    Swagger can be used to test client requests: https://interactivebrokers.github.io/cpwebapi/swagger-ui.html
    Consult curl.trillworks.com for conversion of curl commands to Python requests
    """

    def __init__(self, watchdog_start=True, min_ping_interval_sec=60):
        # NOTE: The ping interval will be longer than specified depending on how long the http request takes to complete
        super().__init__(
            watchdog_start=watchdog_start,
            timeout_sec=min_ping_interval_sec,
            name="IB_HTTP",
        )
        self.name = "HTTP"
        # Base used by all endpoints
        # self.url_http = 'https://localhost:5000/v1/portal'
        self.url_http = "https://localhost:5000/v1/api"
        logger.log(
            "DEBUG", f"Clientportal (HTTP) Started with gateway: {self.url_http}"
        )

        # need to set autostart=False and call after we've defined url_http or we get exceptions due to the watchdog running before things are ready
        # super().start()

    @overrides
    def watchdog_task(self):
        # super().watchdog_task()
        result = self.clientrequest_authentication_status()
        logger.log(
            "DEBUG", f"Watchdog(HTTP): Status: Code:{result.statusCode}, {result.error}"
        )

    # TODO: Add logging wrappers
    async def clientrequest_ping(self):
        """Send session keep-alive."""
        return await self.clientrequest_post(Endpoints.Ping.value)

    async def clientrequest_authentication_status(self):
        """Get current session status."""
        return await self.clientrequest_post(Endpoints.AuthenticationStatus.value)

    async def clientrequest_reauthenticate(self):
        """Re-authenticate a session."""
        return await self.clientrequest_post(Endpoints.Reauthenticate.value)

    async def clientrequest_validate(self):
        """Validate the current session."""
        return await self.clientrequest_get(Endpoints.Validate.value)

    async def clientrequest_logout(self):
        """Log out of current session."""
        return await self.clientrequest_post(Endpoints.Logout.value)

    async def clientrequest_trades(self):
        """Return trades from last current and previous 6 days."""
        return await self.clientrequest_get(Endpoints.Trades.value)

    async def clientrequest_portfolio_accounts(self):
        """Get list of accessible trading accounts."""
        return await self.clientrequest_get(Endpoints.PortfolioAccounts.value)

    async def clientrequest_server_accounts(self):
        """Get list of accessible trading accounts."""
        return await self.clientrequest_get(Endpoints.ServerAccounts.value)

    async def clientrequest_user(self):
        """User connection check"""
        return await self.clientrequest_get(Endpoints.User.value)

    async def clientrequest_search(self, symbol):
        """Get a list of instruments by symbol or name
        Parameters:
            symbol:str = symbol or name
        """
        # NOTE: There is also a secType field which only currently supports 'STK'
        # It doesn't appear to do anything and doesn't fail if it's not passed, so we leave it off for now
        params = {"symbol": symbol, "name": False}
        return await self.clientrequest_post(Endpoints.Search.value, params=params)

    async def clientrequest_search_futures(self, symbols):
        """Get a list of futures based on symbol
        Parameters:
            symbol:str = comma separated list of case-sensitive futures symbols
        """
        params = {"symbols": symbols}
        return await self.clientrequest_post(
            Endpoints.Search_Futures.value, params=params
        )

    async def clientrequest_marketdata(self, conids: str, fields: str = "31"):
        """Request a snapshot of market data
        Parameters:
            conids:str = comma separated list of instrument conids
            fields:str = comma separated list of field codes (see IB docs)
        """
        params = {"conids": conids, "fields": fields}
        return await self.clientrequest_get(Endpoints.Market_Data.value, params=params)

    async def clientrequest_marketdata_history(self, conids: str, period="1min"):
        """Request a snapshot of market data
        Parameters:
            conids:str = comma separated list of instrument conids
            fields:str = comma separated list of field codes (see IB docs)
        """
        params = {"conid": conids, "period": period}
        return await self.clientrequest_get(
            Endpoints.Market_Data_History.value, params=params
        )

    async def clientrequest_switch_account(
        self, env_acct: str = Environment_Var.IB_ACTIVE_ACCOUNT
    ):
        """Change active account (for downloading orders, etc.)
        Parameters: None
           This function uses system environment variables to protect user information
        """
        account = os.environ.get(env_acct, None)

        # Don't bother to call the POST if the account isn't available
        if account is None:
            logger.log("DEBUG", f"{env_acct} not set!")
            return None

        params = {"acctId": account}
        return await self.clientrequest_post(Endpoints.Account.value, params=params)

    async def clientrequest_flexquery_request(self, queryid: str = None):
        """Initiate a flex query request. NOTE: No need to be actively logged in
        Parameters:
            QueryID = IB Assigned number for the flex query (not the name)
            This function uses system environment variables to protect user information
        """
        envar = Environment_Var.IB_FLEXQUERY_TOKEN
        token = os.environ.get(envar, None)

        # Don't bother to call if token is not set
        if token is None:
            logger.log(
                "DEBUG",
                f"System environmental variable '{envar}' not set. No valid IB generated Token!",
            )
            return None

        flexquery_url = f"{IBFlexQuery3.QueryURL}&t={token}&q={queryid}&v=3"
        r = await self.clientrequest_get(flexquery_url, is_ib_endpoint=False)

        try:
            r_xml = r.dict[IBFlexQuery3.XMLFields.FlexStatementResponse]

            # Normally status should be present, but if there is an issue with the request it may not be
            if IBFlexQuery3.XMLFields.Status not in r_xml:
                code = r_xml[IBFlexQuery3.XMLFields.NonVersion3Error]
                logger.log("DEBUG", f"Flex Query Error: '{code}'")
                r.error = IBClientError.Err_FlexQuery_Invalid_Request

            else:
                status = r_xml[IBFlexQuery3.XMLFields.Status]

                if status == IBFlexQuery3.XMLFields.Result_Status.Success:
                    refcode = r_xml[IBFlexQuery3.XMLFields.ReferenceCode]

                    # url is for info purposes only
                    url = r_xml[IBFlexQuery3.XMLFields.Url]
                    received_url = f"{url}&t={token}&q={refcode}&v=3"

                    statement_url = (
                        f"{IBFlexQuery3.GetStatementURL}&t={token}&q={refcode}&v=3"
                    )

                    r = await self.clientrequest_get(
                        statement_url, is_ib_endpoint=False
                    )

                else:
                    errorCode = r_xml[IBFlexQuery3.XMLFields.ErrorCode]
                    errorMessage = r_xml[IBFlexQuery3.XMLFields.ErrorMessage]
                    logger.log(
                        "DEBUG", f"FlexQuery error({errorCode})-'{errorMessage}'"
                    )
                    pass

        except KeyError as e:
            logger.log("DEBUG", f"Unknown FlexQuery key: '{e.args[0]}'")
            r.error = IBClientError.Err_FlexQuery_Key_Not_Found

        except Exception as e:
            logger.log("DEBUG", f"Exception during FlexQuery: {e}")
            r.error = IBClientError.Err_General_Unhandled_Exception

        return r


if __name__ == "__main__":
    print("=== IB Client Portal (HTTP_AIO) ===")
