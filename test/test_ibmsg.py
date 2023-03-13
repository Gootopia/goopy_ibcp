import pytest
from goopy_ibcp.ibmsg_topic import IBTopic
from goopy_ibcp.ibfieldmapper import IBFieldMapper
from goopy_ibcp.ibmsg import IBMsg, IBMsgConverter
from datetime import datetime, timezone
import json


class Test_IBMsgTick:
    """Test class for Tick Messages."""

    utc_timestamp = None

    @classmethod
    def get_test_payload(cls):
        """Create a test payload."""
        dt = datetime(1987, 10, 19, 9, 30)
        utc_time = dt.replace(tzinfo=timezone.utc)
        # Timestamps from IB are in UTC, so we'll keep that format
        cls.utc_timestamp = utc_time.timestamp()
        return IBMsg.payload_dict(cls.utc_timestamp, cls.conid, cls.price)


class Test_IBMsgConverter:
    """Test class for generating system base message."""

    def test_raw_string_is_json(self):
        """Error check that message is a properly formatted JSON string."""
        with pytest.raises(json.JSONDecodeError):
            test_dict: dict = IBMsgConverter.create_dict_from_raw_msg(
                "Not-a-JSON-string"
            )

    def test_topic_exists(self):
        """Error check that IB JSON strings should always have a topic key."""
        with pytest.raises(ValueError):
            test_str = '{"not-a-topic-key": "value"}'
            test_dict, ib_dict = IBMsgConverter.create_dict_from_raw_msg(test_str)

    def test_utc_timestamp_exists(self):
        """Error check to make sure that we are getting '_updated' (UTC timestamp)."""
        with pytest.raises(ValueError):
            test_str = '{"topic": "value"}'
            test_dict, ib_dict = IBMsgConverter.create_dict_from_raw_msg(test_str)

    def test_payload_decode(self):
        """Verify that converter pulls out the correct fields/values for the payload dict."""
        test_dict, ib_dict = IBMsgConverter.create_dict_from_raw_msg(
            IBMsgConverter._get_test_string()
        )

        assert IBFieldMapper.Time in test_dict.keys()
        assert test_dict[IBFieldMapper.Time] == 1678284754734
