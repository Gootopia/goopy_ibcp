"""One-stop error code farm for all kinds of errors"""

from enum import Enum, unique


@unique
class Error(Enum):
    """Descriptive Error Strings"""

    # GENERAL ERROR MESSAGES
    Unhandled_Exception = -1
    No_Error = 1
    Invalid_URL = 2
    # Connection_or_Timeout = 3

    # JSON ISSUES
    Err_JSON_Invalid_Format = 100

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


if __name__ == "__main__":
    print("=== error.py ===")
