from overrides import overrides
from loguru import logger

from goopy_ibcp.endpoints import Endpoints
from goopy_ibcp.httpendpoints import HttpEndpoints


class ClientPortalHttp(HttpEndpoints):
    # TODO: Document ClientPortalHttp class
    """
    Interactive Brokers ClientPortal Interface (HTTP).
    Refer to https://www.interactivebrokers.com/api/doc.html for API documentation
    Swagger can be used to test client requests: https://interactivebrokers.github.io/cpwebapi/swagger-ui.html
    Consult curl.trillworks.com for conversion of curl commands to Python requests
    """
    def __init__(self, watchdog_start=True, min_ping_interval_sec=60):
        # NOTE: The ping interval will be longer than specified depending on how long the http request takes to complete
        super().__init__(watchdog_start=watchdog_start, timeout_sec=min_ping_interval_sec, name='IB_HTTP')
        self.name = 'HTTP'
        # Base used by all endpoints
        #self.url_http = 'https://localhost:5000/v1/portal'
        self.url_http = 'https://localhost:5000/v1/api'
        logger.log('DEBUG', f'Clientportal (HTTP) Started with gateway: {self.url_http}')

        # need to set autostart=False and call after we've defined url_http or we get exceptions due to the watchdog running before things are ready
        #super().start()

    @overrides
    def watchdog_task(self):
        # super().watchdog_task()
        result = self.clientrequest_authentication_status()
        logger.log('DEBUG', f'Watchdog(HTTP): Status: Code:{result.statusCode}, {result.error}')

    # TODO: Add logging wrappers
    def clientrequest_ping(self):
        """ Send session keep-alive."""
        return self.clientrequest_post(Endpoints.Ping.value)

    def clientrequest_authentication_status(self):
        """ Get current session status."""
        return self.clientrequest_post(Endpoints.AuthenticationStatus.value)

    def clientrequest_reauthenticate(self):
        """ Re-authenticate a session."""
        return self.clientrequest_post(Endpoints.Reauthenticate.value)

    def clientrequest_validate(self):
        """ Validate the current session."""
        return self.clientrequest_get(Endpoints.Validate.value)

    def clientrequest_logout(self):
        """ Log out of current session. """
        return self.clientrequest_post(Endpoints.Logout.value)

    def clientrequest_trades(self):
        """ Return trades from last current and previous 6 days."""
        return self.clientrequest_get(Endpoints.Trades.value)

    def clientrequest_brokerage_accounts(self):
        """ Get list of accessible trading accounts."""
        return self.clientrequest_get(Endpoints.BrokerageAccounts.value)

    def clientrequest_search(self, symbol):
        """ Get a list of instruments by symbol or name
        Parameters:
            symbol:str = symbol or name
        """
        # NOTE: There is also a secType field which only currently supports 'STK'
        # It doesn't appear to do anything and doesn't fail if it's not passed, so we leave it off for now
        params = {"symbol" : symbol, "name": False}
        return self.clientrequest_post(Endpoints.Search.value, params=params)

    def clientrequest_search_futures(self, symbols):
        """ Get a list of futures based on symbol
        Parameters:
            symbol:str = comma separated list of case-sensitive futures symbols
        """
        params = {"symbols" : symbols}
        return self.clientrequest_post(Endpoints.Search_Futures.value, params=params)

    def clientrequest_marketdata(self, conids:str, fields:str="31"):
        """ Request a snapshot of market data
        Parameters:
            conids:str = comma separated list of instrument conids
            fields:str = comma separated list of field codes (see IB docs)
        """
        params = {"conids" : conids, "fields" : fields}
        return self.clientrequest_get(Endpoints.Market_Data.value, params=params)

    def clientrequest_marketdata_history(self, conids:str, period="1min"):
        """ Request a snapshot of market data
        Parameters:
            conids:str = comma separated list of instrument conids
            fields:str = comma separated list of field codes (see IB docs)
        """
        params = {"conid" : conids, "period" : period}
        return self.clientrequest_get(Endpoints.Market_Data_History.value, params=params)

if __name__ == '__main__':
    print("=== IB Client Portal (HTTP) ===")
