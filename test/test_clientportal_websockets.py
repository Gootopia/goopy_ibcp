import pytest
from unittest.mock import patch

# from goopy_certificate.certificate import CertificateError, CertificateReturn
from goopy_ibcp.certificate import CertificateError, CertificateReturn
from goopy_ibcp.ibfieldmapper import IBFieldMapper
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase
from goopy_ibcp.error import IBClientError


class TestClientPortalWebSocketsNotPatched:
    """Test class for ClientPortalWebSockets methods that don't need patching"""

    def test_build_smd_string_good(self):
        """Verify we can make a good string from test info"""
        conid = "12345678"
        tick_types = ["12", "13", "14"]
        # Note that these aren't valid tick types or conid, but right now we only care about format
        good_str = 'smd+12345678+{"fields":["12","13","14"]}'
        result, smd_str = ClientPortalWebsocketsBase._build_ws_str_smd(
            conid, tick_types
        )
        assert result == IBClientError.Err_General_Ok
        assert smd_str == good_str

    def test_build_smd_string_bad_conid(self):
        """Check that we pass only a numeral as conid"""
        conid = "bad"
        result = ClientPortalWebsocketsBase._build_ws_str_smd(conid, None)
        assert result == IBClientError.Err_MarketData_Conid_Invalid

    def test_tick_types_good(self):
        """Check that we ignore any unknown tick types"""
        ticks_requested = [
            "99",
            IBFieldMapper.Price_Ask,
            "garbage",
            IBFieldMapper.Price_Bid,
            IBFieldMapper.Price_Close,
            "junk",
            None,
            12345,
            IBFieldMapper.Price_High,
            IBFieldMapper.Price_Last,
            IBFieldMapper.Price_Low,
            IBFieldMapper.Price_Open,
        ]
        ticks_used = ClientPortalWebsocketsBase._check_tick_types(ticks_requested)

        # Only valid types should show up in the return
        assert IBFieldMapper.Price_Ask in ticks_used
        assert IBFieldMapper.Price_Bid in ticks_used
        assert IBFieldMapper.Price_Close in ticks_used
        assert IBFieldMapper.Price_High in ticks_used
        assert IBFieldMapper.Price_Last in ticks_used
        assert IBFieldMapper.Price_Low in ticks_used
        assert IBFieldMapper.Price_Open in ticks_used


@patch("goopy_ibcp.clientportal_websockets.Certificate.get_certificate")
class TestClientPortalWebsocketsPatched:
    """Test class for ClientPortalWebsockets methods which need patching"""

    @staticmethod
    def url_validator_ok(url=""):
        """Simulate checking a URL and finding it valid"""
        return True

    @staticmethod
    def url_validator_invalid(url=""):
        """Simulate checking a URL and finding it bad"""
        return False

    @pytest.mark.asyncio
    async def test_open_connection_invalid_url(self, patched):
        cp = ClientPortalWebsocketsBase()
        result = await cp.__open_connection(
            url_validator=TestClientPortalWebsockets.url_validator_invalid
        )
        assert result == IBClientError.Err_General_Invalid_URL

    @pytest.mark.asyncio
    async def test_open_connection_invalid_certificate(self, patched):
        patched.return_value = CertificateReturn(
            None, CertificateError.Invalid_Certificate
        )
        cp = ClientPortalWebsocketsBase()
        result = await cp.__open_connection()
        assert result == IBClientError.Err_Websocket_Invalid_Certificate

    @pytest.mark.asyncio
    async def test_open_connection_failed(self, patched):
        patched.return_value = CertificateReturn(None, CertificateError.Ok)
        cp = ClientPortalWebsocketsBase()
        result = await cp.__open_connection()
        assert result == IBClientError.Err_Websocket_Invalid_Certificate
