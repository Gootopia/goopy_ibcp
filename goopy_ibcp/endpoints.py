# Interactive Brokers Client Portal Web API endpoints and other various convenience classes
# See: https://www.interactivebrokers.com/api/doc.html
from enum import Enum


class Endpoints(Enum):
    Blank = ""
    # SESSION ENDPOINTS
    Ping = "/tickle"
    AuthenticationStatus = "/iserver/auth/status"
    Reauthenticate = "/iserver/reauthenticate"
    Validate = "/sso/validate"
    Logout = "/logout"
    User = "/one/user"

    # TRADE ENDPOINTS
    Trades = "/iserver/account/trades"

    # CONTRACT/SEARCH ENDPOINTS
    Search = "/iserver/secdef/search"
    Search_Futures = "/trsrv/futures"

    # ACCOUNT ENDPOINTS
    PortfolioAccounts = "/portfolio/accounts"
    ServerAccounts = "/iserver/accounts"
    # This endpoint is for selecting the active account
    Account = "/iserver/account"

    # ORDERS
    LiveOrders = "/iserver/account/orders"

    # MARKET DATA
    Market_Data = "/iserver/marketdata/snapshot"
    # Market_Data = '/md/snapshot'
    Market_Data_History = "/iserver/marketdata/history"
