"""One-stop error code farm for all kinds of errors"""

from enum import Enum, unique


@unique
class Error(Enum):
    """Descriptive Error Strings"""

    # General error messages
    Unhandled_Exception = -1
    No_Error = 1
    Invalid_URL = 2
    Connection_or_Timeout = 3

    # JSON Issues
    JSONErr_Invalid_Format = 100

    # Account Issues
    AccountErr_No_Accounts_Key_Found = 200


if __name__ == "__main__":
    print("=== error.py ===")
