"""One-stop error code farm for all kinds of errors"""

from enum import Enum, unique


@unique
class IBClientError(Enum):
    """Descriptive IB Client Error Strings"""

    # GENERAL ERROR MESSAGES
    Err_General_Unhandled_Exception = -1
    Err_General_Ok = 1
    Err_General_Invalid_URL = 2

    # JSON ISSUES
    Err_Json_Invalid_Format = 100

    # ACCOUNT ISSUES
    Err_Account_No_Accounts_Key_Found = 200

    # CONNECTION ISSUES
    Err_Connection_No_Gateway = 300
    Err_Connection_Timeout = 301
    Err_Connection_Incomplete_WebRequest_401 = 302
    Err_Connection_Unauthorized_Web_Request_403 = 303
    # This one may be observed if we try and switch to an already selected account
    Err_Connection_Internal_Error_500 = 304
    Err_Connection_Unhandled_Web_Error = 305

    # TRADE ISSUES
    Err_Trades_No_Trades_Found = 400

    # FLEXQUERY
    Err_FlexQuery_Invalid_Request = 500
    Err_FlexQuery_Key_Not_Found = 501

    # MARKET DATA
    Err_MarketData_Conid_Not_Integer = 600
    Err_MarketData_Conid_Invalid = 601

    # WEBSOCKET
    Err_Websocket_Unhandled_Exception = 700
    Err_Websocket_Invalid_Certificate = 701
    Err_Websocket_Connection_Failed = 702
    Err_Websocket_Connection_Refused = 703
    Err_Websocket_Connection_Closed = 704
    Err_Websocket_Missing_Key = 705


if __name__ == "__main__":
    print("=== error.py ===")
