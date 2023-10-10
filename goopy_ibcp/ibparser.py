"""IB JSON Parser.

Parse JSON structures returned by ClientPortal to extract desired items (trades, accounts, etc.)
"""
import json

from goopy_ibcp.ibmodels import IBModels
from goopy_ibcp.error import Error


class IBParser:
    """IB Parser for extracting info from Clientportal JSON structures"""

    @staticmethod
    def get_accounts(jsonstr: str = None):
        """Check for presence of accounts in the json string"""
        try:
            # Dumps will only pass if we have a valid json dictionary
            convert = json.dumps(jsonstr)

            # Now try and find the accounts key
            accounts = jsonstr[IBModels.ClientRequest_User.Accounts]

        except TypeError as e:
            return None, Error.JSONErr_Invalid_Format

        except KeyError as e:
            return None, Error.AccountErr_No_Accounts_Key_Found

        except Exception as e:
            return None, Error.Unhandled_Exception

        return accounts, Error.No_Error
