import pytest
import json

from goopy_ibcp.jsonmsg import JSONMsg

# Requirement
# - Topic input can't be empty (ValueError)
# - Payload input is dictionary of key-value pairs (TypeError)
# - Payload output is a JSON string
# - Method to build transmit string from topic + payload
# - Transmit packet out is string with format "topic&&{JSON}"


class Test_JSONMsg:
    """Test class for JSONMsg."""

    def test_topic_not_empty(self):
        """Message topics must be set."""
        with pytest.raises(ValueError):
            msg = JSONMsg()

        with pytest.raises(ValueError):
            msg = JSONMsg(None)

    def test_topic_stored(self):
        """Topic must be stored in instance."""
        msg = JSONMsg("newtopic")
        assert msg.topic == "newtopic"

    def test_separator_stored(self):
        """Separator must be stored in instance."""
        msg = JSONMsg("newtopic")
        assert msg.separator == "&&"

    def test_payload_not_none(self):
        """Payload can't be empty."""
        with pytest.raises(ValueError):
            formatted_payload = JSONMsg.format_payload(None)

    def test_payload_formatter(self):
        """Verify payload formatter output."""
        topic = "topic"
        msg = JSONMsg(topic)
        payload = {"p1": "value1", "p2": "value2"}
        payload_json = json.dumps(payload)

        payload_formatted = JSONMsg.format_payload(payload)
        assert payload_formatted == payload_json

    def test_build_msg(self):
        """Verify transmit msg format {topic}{separator}{json_payload}."""
        topic = "topic"
        msg = JSONMsg(topic)
        payload = {"p1": "value1", "p2": "value2"}
        payload_json = json.dumps(payload)
        packet = msg.build_message(payload)
        good_result = f"{topic}{msg.separator}{payload_json}"
        assert packet == good_result
