# Various error codes for ib client

from enum import Enum, unique


@unique
class Error(Enum):
    No_Error = 1
    Invalid_URL = 2
    Connection_or_Timeout = 3


if __name__ == '__main__':
    print("=== error.py ===")