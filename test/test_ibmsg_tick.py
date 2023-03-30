"""Test classes for IBMsgTick/IBMsgConverterTick."""

import pytest
from goopy_ibcp.ibfieldmapper import IBFieldMapper
from goopy_ibcp.ibmsg_tick import IBMsgTick, IBMsgConverterTick


class Test_IBMsgTick:
    """Test class for Tick Messages."""

    def test_payload_decoder(self):
        """Check the build payload function."""
        assert False


class TestIBMsgConverterTick:
    """Test class for generating system message traffic from raw IB tick traffic."""

    def test_required_keys(self):
        """Verify that message has properly specified all its required keys."""
        # NOTE: Price data keys are check further down
        assert IBFieldMapper.Topic in IBMsgConverterTick.required_keys
        assert IBFieldMapper.Conid in IBMsgConverterTick.required_keys
        assert IBFieldMapper.Time in IBMsgConverterTick.required_keys

    def test_key_verification(self):
        """Verify that message actually catches the missing keys."""
        test_dict = {"key1": "value1", "key2": "value2"}
        missing_keys = IBMsgConverterTick.verify_keys(test_dict)
        assert IBFieldMapper.Topic in missing_keys
        assert IBFieldMapper.Conid in missing_keys
        assert IBFieldMapper.Time in missing_keys

    def test_correct_topic(self):
        """Make sure converter is checking for the correct topic."""
        test_str = IBMsgConverterTick._get_test_tick_string()
        test_dict = IBMsgConverterTick._get_test_dict(test_str)

        assert IBMsgConverterTick.verify_msg_topic(test_dict, "smd", exact_match=False)

    def test_price_data_exists(self):
        """Error check to make sure that we are getting some price data with this message."""
        with pytest.raises(ValueError):
            # Test message with no price data to cause an error.
            test_str = '{"topic": "value", "_updated" : "12345678", "conid" : "1234"}'
            test_dict = IBMsgConverterTick.create_dict_from_raw_msg(test_str)

    def test_payload_decode(self):
        """Verify that converter pulls out correct fields from example string."""
        test_dict: dict = IBMsgConverterTick.create_dict_from_raw_msg(
            IBMsgConverterTick._get_test_tick_string()
        )

        # Make sure we extracted what we want from raw IB json message. See test string in IBMsgConverterTick
        assert IBFieldMapper.Conid in test_dict.keys()
        assert test_dict[IBFieldMapper.Conid] == 495512572
        assert IBFieldMapper.Time in test_dict.keys()
        assert test_dict[IBFieldMapper.Time] == 1678666665031
        assert IBFieldMapper.Price_Last in test_dict.keys()
        assert test_dict[IBFieldMapper.Price_Last] == "3913.50"
        assert IBFieldMapper.Price_Ask in test_dict.keys()
        assert test_dict[IBFieldMapper.Price_Ask] == "3913.75"
        assert IBFieldMapper.Price_Bid in test_dict.keys()
        assert test_dict[IBFieldMapper.Price_Bid] == "3913.25"
