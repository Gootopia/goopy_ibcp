# Interactive Brokers Client Portal Web API endpoints and other various convenience classes
# See: https://www.interactivebrokers.com/api/doc.html
from enum import Enum


class Endpoints(Enum):
    Blank = ''
    # SESSION ENDPOINTS
    Ping = '/tickle'
    AuthenticationStatus = '/iserver/auth/status'
    Reauthenticate = '/iserver/reauthenticate'
    Validate = '/sso/validate'
    Logout = '/logout'
    
    # TRADE ENDPOINTS
    Trades = '/iserver/account/trades'

    # CONTRACT/SEARCH ENDPOINTS
    Search = '/iserver/secdef/search'
    Search_Futures = '/trsrv/futures'

    # ACCOUNT ENDPOINTS
    BrokerageAccounts = '/iserver/accounts'

    # MARKET DATA
    Market_Data = '/iserver/marketdata/snapshot'
    Market_Data_History = '/iserver/marketdata/history'