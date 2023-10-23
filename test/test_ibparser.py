import pytest
from goopy_ibcp.ibparser import IBParser
from goopy_ibcp.error import Error


class Test_IBParser:
    """Test class for IB Clientportal JSON Parsers"""

    def test_get_accounts_bad_json_format(self):
        """Catch when passed data has issues with JSON format"""
        not_json_string = "not_json"

        acct, err = IBParser.get_accounts(not_json_string)
        assert err == Error.Err_JSON_Invalid_Format
        assert acct is None

        bad_json_format = {"key"}

        acct, err = IBParser.get_accounts(bad_json_format)
        assert err == Error.Err_JSON_Invalid_Format
        assert acct is None
        return

    def test_get_accounts_no_account_info(self):
        """Catch when JSON string doesn't have the account key"""
        no_accounts = {"noaccountkey": "goodvalue"}

        acct, err = IBParser.get_accounts(no_accounts)
        assert err == Error.Err_Account_No_Accounts_Key_Found
        assert acct is None
        return

    def test_get_accounts_check_accounts(self):
        """Verify the accounts passed from a valid JSON string with that info"""
        test_msg = Test_IBParser.TestMessages.clientrequest_user
        accounts, err = IBParser.get_accounts(test_msg)
        assert err == Error.No_Error
        assert "U1111111" in accounts
        assert "U2222222" in accounts
        return

    def test_get_trades_bad_json_format(self):
        """Catch when passed data has issues with JSON format"""
        not_json_string = "not_json"

        acct, err = IBParser.get_trades(not_json_string)
        assert err == Error.Err_JSON_Invalid_Format
        assert acct is None

        bad_json_format = {"key"}

        acct, err = IBParser.get_trades(bad_json_format)
        assert err == Error.Err_JSON_Invalid_Format
        assert acct is None
        return

    def test_get_trades_no_trade_info(self):
        """Catch when JSON string doesn't have the account key"""
        no_accounts = {"noaccountkey": "goodvalue"}

        acct, err = IBParser.get_trades(no_accounts)
        assert err == Error.Err_Trades_No_Trades_Found
        assert acct is None
        return

    def test_get_trades_check_trades(self):
        """Verify the accounts passed from a valid JSON string with that info"""
        test_msg = Test_IBParser.TestMessages.clientrequest_trades

        trades, err = IBParser.get_trades(test_msg)
        assert err == Error.No_Error
        return

    # BELOW HERE ARE EXAMPLE JSON STRINGS (At the end for readability)
    # Test string extracted from a call to clientrequest_user. Account info redacted
    # This has an open and a closed account (there are others...see IB docs)
    class TestMessages:
        """Test JSON strings which can be received from various endpoints"""

        clientrequest_user: str = {
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
        # This has examples of a buy (B), sell (S), and expire (X) executed trades. Account info redacted

        clientrequest_trades: str = [
            {
                "execution_id": "00019123.65240d41.01.01",
                "symbol": "MES",
                "supports_tax_opt": "1",
                "side": "S",
                "order_description": "Sold 1 @ 10.75 on CME",
                "trade_time": "20231009-20:12:14",
                "trade_time_r": 1696882334000,
                "size": 1.0,
                "price": "10.75",
                "order_ref": "OptTrader",
                "exchange": "CME",
                "net_amount": 53.75,
                "account": "AccountAlias",
                "accountCode": "U1234567",
                "company_name": "Micro E-Mini S&P 500 Stock Price Index",
                "contract_description_1": "MES",
                "contract_description_2": "(EX2) OCT23 4300 Put Fut. Option",
                "sec_type": "FOP",
                "conid": 652847924,
                "conidEx": "652847924@CME",
                "clearing_id": "IB",
                "clearing_name": "IB",
                "open_close": "???",
                "liquidation_trade": "0",
                "is_event_trading": "0",
                "commission": "0.47",
            },
            {
                "execution_id": "00019123.6520645f.01.01",
                "symbol": "MES",
                "supports_tax_opt": "1",
                "side": "B",
                "order_description": "Bot 2 @ 4346.00 on CME",
                "trade_time": "20231006-20:05:27",
                "trade_time_r": 1696622727000,
                "size": 2.0,
                "price": "4346.00",
                "exchange": "CME",
                "net_amount": 43460.0,
                "account": "AccountAlias",
                "accountCode": "U1234567",
                "company_name": "Micro E-Mini S&P 500 Stock Price Index",
                "contract_description_1": "MES DEC23",
                "sec_type": "FUT",
                "listing_exchange": "CME",
                "conid": 586139726,
                "conidEx": "586139726@CME",
                "clearing_id": "IB",
                "clearing_name": "IB",
                "liquidation_trade": "0",
                "is_event_trading": "0",
                "commission": "1.24",
            },
            {
                "execution_id": "000192ba.6520e7aa.01.01",
                "symbol": "MES",
                "supports_tax_opt": "1",
                "side": "X",
                "order_description": "EXPIRED 2 on CME",
                "trade_time": "20231007-05:11:25",
                "trade_time_r": 1696655485000,
                "size": 2.0,
                "price": "0.0",
                "exchange": "CME",
                "net_amount": 0.0,
                "account": "AccountAlias",
                "accountCode": "U1234567",
                "company_name": "",
                "contract_description_1": "MES",
                "contract_description_2": "(EX1) OCT23 4185 Put Fut. Option",
                "sec_type": "FOP",
                "conid": 656795538,
                "conidEx": "656795538@CME",
                "open_close": "???",
                "liquidation_trade": "0",
                "is_event_trading": "0",
            },
        ]
