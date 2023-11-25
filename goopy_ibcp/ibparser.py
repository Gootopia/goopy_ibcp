"""IB JSON Parser.

Parse JSON structures returned by ClientPortal to extract desired items (trades, accounts, etc.)
"""
import json

from ibmodels import IBModels
from error import IBClientError


class IBParser:
    """IB Parser for extracting info from Clientportal JSON structures"""

    @staticmethod
    def get_accounts(jsonstr: str = None):
        """Get a list of accounts in the json string (if present)"""
        try:
            # Dumps will only pass if we have a valid json dictionary
            convert = json.dumps(jsonstr)

            # Now try and find the accounts key
            accounts = jsonstr[IBModels.User.Accounts]

        except TypeError as e:
            return None, IBClientError.Err_JSON_Invalid_Format

        except KeyError as e:
            return None, IBClientError.Err_Account_No_Accounts_Key_Found

        except Exception as e:
            return None, IBClientError.Unhandled_Exception

        return accounts, IBClientError.Ok

    @staticmethod
    def get_trades(jsonstr: str = None):
        """Extract a list of trades from a string (if present)"""
        try:
            # Dumps will only pass if we have a valid json dictionary
            convert = json.dumps(jsonstr)

            trades: list = []

            # Trades are just a list of executions, so we
            for trade in jsonstr:
                if IBModels.Trade.Trade_Execution in trade:
                    trades.insert(0, trade)

            if len(trades) == 0:
                return None, IBClientError.Err_Trades_No_Trades_Found

        except TypeError as e:
            return None, IBClientError.Err_JSON_Invalid_Format

        except Exception as e:
            return None, IBClientError.Unhandled_Exception

        return trades, IBClientError.Ok
