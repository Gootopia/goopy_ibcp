import pytest
from goopy_ibcp.ibparser import IBParser
from goopy_ibcp.error import Error


class Test_IBParser:
    """Test class for IB Clientportal JSON Parsers"""

    # Test string extracted from a call to clientrequest_user. Account info redacted
    # This has an open and a closed account (there are others...see IB docs)
    testmsg_clientrequest_user: str = {
        "wbId": "",
        "ispaper": False,
        "islite": False,
        "has2fa": True,
        "username": "testuser",
        "features": {
            "env": "P\OD",
            "wlms": True,
            "realtime": True,
            "bond": True,
            "optionChains": True,
            "calendar": True,
            "newMf": True,
        },
        "applicants": [
            {
                "id": 123456,
                "type": "INDIVIDUAL",
                "entityId": 1234567,
                "businessType": "INDEPENDENT",
                "legalCountry": {"name": "United States", "alpha3": "USA"},
                "nlcode": "en",
            }
        ],
        "uar": {
            "portfolioAnalyst": True,
            "userInfo": True,
            "messageCenter": True,
            "accountDetails": True,
            "tradingRestrictions": False,
            "tws": True,
            "fyi": True,
            "voting": True,
            "forum": True,
            "recentTransactions": True,
        },
        "accts": {
            "U1111111": {
                "clearingStatus": "O",
                "openDate": 1389848400000,
                "isFunded": True,
                "tradingPermissions": [
                    "OPT",
                    "FUT",
                    "FOP",
                    "WAR",
                    "STK",
                    "CASH",
                    "COMB",
                ],
                "isFAClient": False,
            },
            "U2222222": {
                "clearingStatus": "C",
                "openDate": 1301630400000,
                "isFunded": True,
                "tradingPermissions": [],
                "isFAClient": False,
            },
        },
        "props": {"readOnlySession": None, "isIBAMClient": False},
        "firstApprovedDate": 1301889600000,
    }

    def test_get_accounts_bad_json_format(self):
        """Catch when passed data has issues with JSON format"""
        not_json_string = "not_json"

        acct, err = IBParser.get_accounts(not_json_string)
        assert err == Error.JSONErr_Invalid_Format
        assert acct is None

        bad_json_format = {"key"}

        acct, err = IBParser.get_accounts(bad_json_format)
        assert err == Error.JSONErr_Invalid_Format
        assert acct is None
        return

    def test_get_accounts_no_account_info(self):
        """Catch when JSON string doesn't have the account key"""
        no_accounts = {"noaccountkey": "goodvalue"}

        acct, err = IBParser.get_accounts(no_accounts)
        assert err == Error.AccountErr_No_Accounts_Key_Found
        assert acct is None
        return

    def test_get_accounts_check_accounts(self):
        """Verify the accounts passed from a valid JSON string with that info"""
        test_msg = Test_IBParser.testmsg_clientrequest_user
        accounts, err = IBParser.get_accounts(test_msg)
        assert err == Error.No_Error
        assert "U1111111" in accounts
        assert "U2222222" in accounts
        return
