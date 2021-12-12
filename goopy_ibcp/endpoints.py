# Interactive Brokers Client Portal Web API endpoints
# See: https://www.interactivebrokers.com/api/doc.html
from enum import Enum


class Endpoints(Enum):
    Blank = ''
    # SESSION ENDPOINTS
    Ping = '/tickle'
    AuthenticationStatus = '/iserver/auth/status'
    Reauthenticate = '/iserver/reauthenticate'
    Validate = '/sso/validate'
    # TRADE ENDPOINTS
    Trades = '/iserver/account/trades'

    # CONTRACT/SEARCH ENDPOINTS
    Search = '/iserver/secdef/search'

    # ACCOUNT ENDPOINTS
    BrokerageAccounts = '/iserver/accounts'