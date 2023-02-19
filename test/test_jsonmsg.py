import pytest
import json

from goopy_ibcp.jsonpacket import JSONPacket

# Requirement
# - Topic input can't be empty (ValueError)
# - Payload input is dictionary of key-value pairs (TypeError)
# - Payload output is a JSON string
# - Method to build transmit string from topic + payload
# - Transmit packet out is string with format "topic&&{JSON}"


class Test_JSONMsg:
    """Test class for JSONMsg."""

    # Some convenience stuff so we don't need to keep defining it
    new_topic = "topic"
    new_payload: dict = {"p1": "value1", "p2": "value2"}

    @staticmethod
    def get_test_message():
        """Define a convenience test message to avoid DRY."""
        return JSONPacket(Test_JSONMsg.new_topic, Test_JSONMsg.new_payload)

    def test_topic_is_set(self):
        """Message topic must be set."""
        with pytest.raises(ValueError):
            # Can't be empty (default is "")
            msg = JSONPacket()

        with pytest.raises(ValueError):
            # Also can't be None
            msg = JSONPacket(None)

    def test_topic_stored(self):
        """Topic must be stored in instance."""
        msg = Test_JSONMsg.get_test_message()
        assert msg.topic == "topic"

    def test_separator_stored(self):
        """Separator must be stored in instance."""
        msg = Test_JSONMsg.get_test_message()
        # This is the same separator the IB uses in their messages (see docs)
        assert msg.separator == JSONPacket.PacketSeparator
        assert msg.separator == "+"

    def test_msg_stored(self):
        """Payload must be stored in the instance."""
        msg = Test_JSONMsg.get_test_message()
        assert msg.payload == Test_JSONMsg.new_payload

    def test_payload_formatter(self):
        """Verify payload formatter output converts dict to json."""
        payload_json = json.dumps(Test_JSONMsg.new_payload)
        payload_formatted = JSONPacket.format_payload(Test_JSONMsg.new_payload)
        assert payload_formatted == payload_json

    def test_format_empty_payload(self):
        """Verify that no payload translates to empty json string."""
        empty_json = json.dumps({})
        empty_formatted = JSONPacket.format_payload({})
        assert empty_formatted == empty_json

        # Also test that a payload of None gives empty json
        assert JSONPacket.format_payload(None) == empty_json

    def test_build_and_store_packet(self):
        """Verify transmit msg format {topic}{separator}{json_payload}."""
        msg = Test_JSONMsg.get_test_message()
        payload_json = json.dumps(Test_JSONMsg.new_payload)
        formatted_packet = msg.build_packet()
        good_result = f"{Test_JSONMsg.new_topic}{msg.separator}{payload_json}"
        assert formatted_packet == good_result
        assert formatted_packet == msg.formatted_packet

    def test_get_packet_payload(self):
        """Recover the packet payload in dict format."""
        msg = Test_JSONMsg.get_test_message()
        formatted_packet = msg.build_packet()
        payload_dict = msg.get_packet_payload(formatted_packet)
        assert payload_dict["p1"] == "value1"
        assert payload_dict["p2"] == "value2"
