"""Test classes for IBMsgTick/IBMsgConverterTick."""

import pytest
from goopy_ibcp.ibmsg_topic import IBTopic
from goopy_ibcp.ibfieldmapper import IBFieldMapper
from goopy_ibcp.ibmsg_tick import IBMsgTick, IBMsgConverterTick
from datetime import datetime, timezone


class Test_IBMsgTick:
    """Test class for Tick Messages."""

    conid: str = "495512572"
    price: str = "2000.00"
    utc_timestamp = None

    @classmethod
    def get_test_payload(cls) -> dict:
        """Create a test payload."""
        dt = datetime(1987, 10, 19, 9, 30)
        utc_time = dt.replace(tzinfo=timezone.utc)
        # Timestamps from IB are in UTC, so we'll keep that format
        cls.utc_timestamp = utc_time.timestamp()
        return IBMsgTick.payload_dict(cls.utc_timestamp, cls.conid, cls.price)

    def test_payload_decoder(self):
        """Check the build payload function."""
        assert False


class TestIBMsgConverterTick:
    """Test class for generating system message traffic from raw IB tick traffic."""

    def test_conid_exists(self):
        """Error check to make sure that we are getting the contract id (conid)."""
        with pytest.raises(ValueError):
            # Test message with no conid to cause an error.
            test_str = '{"topic": "value", "_updated" : "12345678"}'
            test_dict = IBMsgConverterTick.create_dict_from_raw_msg(test_str)

    def test_price_data_exists(self):
        """Error check to make sure that we are getting some price data with this message."""
        with pytest.raises(ValueError):
            # Test message with no price data to cause an error.
            test_str = '{"topic": "value", "_updated" : "12345678", "conid" : "1234"}'
            test_dict = IBMsgConverterTick.create_dict_from_raw_msg(test_str)

    def test_payload_decode(self):
        """Verify that converter pulls out correct fields from example string."""
        test_dict: dict = IBMsgConverterTick.create_dict_from_raw_msg(
            IBMsgConverterTick._get_test_string()
        )

        # Make sure we extracted what we want from raw IB json message. See test string in IBMsgConverterTick
        assert IBFieldMapper.Conid in test_dict.keys()
        assert test_dict[IBFieldMapper.Conid] == 495512572
        assert IBFieldMapper.Price_Last in test_dict.keys()
        assert test_dict[IBFieldMapper.Price_Last] == "3913.50"
        assert IBFieldMapper.Price_Ask in test_dict.keys()
        assert test_dict[IBFieldMapper.Price_Ask] == "3913.75"
        assert IBFieldMapper.Price_Bid in test_dict.keys()
        assert test_dict[IBFieldMapper.Price_Bid] == "3913.25"
