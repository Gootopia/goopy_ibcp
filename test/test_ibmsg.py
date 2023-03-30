import pytest
from goopy_ibcp.ibmsg_topic import IBTopic
from goopy_ibcp.ibfieldmapper import IBFieldMapper
from goopy_ibcp.ibmsg import IBMsg, IBMsgConverter
from datetime import datetime, timezone
import json


class Test_IBMsgTick:
    """Test class for Tick Messages."""


class Test_IBMsgConverter:
    """Test class for generating system base message."""

    def test_raw_string_is_json(self):
        """Error check that message is a properly formatted JSON string."""
        with pytest.raises(json.JSONDecodeError):
            test_dict: dict = IBMsgConverter.create_dict_from_raw_msg(
                "Not-a-JSON-string"
            )

    def test_missing_keys(self):
        """Error check that we can flag any required keys are missing in a message dictionary."""
        test_tick_str = IBMsgConverter._get_test_tick_string()
        ib_msg_dict = IBMsgConverter.create_dict_from_raw_msg(test_tick_str)
        missing_keys = IBMsgConverter._check_keys(
            ib_msg_dict, required_keys=["badkey1", "badkey2"]
        )
        assert "badkey1" in missing_keys
        assert "badkey2" in missing_keys

    def test_msg_topic_is_substring(self):
        """Verify we can check if desired topic is sub-string of message topic."""
        test_str = IBMsgConverter._get_test_tick_string()
        test_dict = IBMsgConverter._get_test_dict(test_str)

        assert IBMsgConverter.verify_msg_topic(test_dict, "smd", exact_match=False)

    def test_msg_topic_is_exact_match(self):
        """Verify we can check if desired topic is an exact match of message topic."""
        test_str = IBMsgConverter._get_test_tick_string()
        test_dict = IBMsgConverter._get_test_dict(test_str)

        assert IBMsgConverter.verify_msg_topic(
            test_dict, "smd+495512572", exact_match=True
        )

    def test_msg_topic_no_match(self):
        """Error check when no match is found either exact or as sub-string."""
        test_str = IBMsgConverter._get_test_tick_string()
        test_dict = IBMsgConverter._get_test_dict(test_str)

        # no matching substring in topic
        assert (
            IBMsgConverter.verify_msg_topic(test_dict, "bad_topic", exact_match=False)
            == False
        )
        # no exact match in topic
        assert (
            IBMsgConverter.verify_msg_topic(test_dict, "bad_topic", exact_match=True)
            == False
        )
