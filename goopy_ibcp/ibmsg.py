"""IB Message.

Base message from which other messages are derived.
"""
from goopy_ibcp.jsonpacket import JSONPacket
from goopy_ibcp.ibmsg_topic import IBTopic
from goopy_ibcp.ibfieldmapper import IBFieldMapper
import json


class IBMsg(JSONPacket):
    """System message for tick data received from IB quote server."""

    def create_topic(self, payload: dict):
        """Generate a message topic."""
        raise NotImplementedError(
            "create_topic() must be overriden to provide actual message topic!"
        )

    def __init__(self, payload: dict) -> None:
        """IBMsg constructor."""
        tick_topic = self.create_topic(self, payload)
        super().__init__(tick_topic, payload)


class IBMsgConverter:
    """Common fields which are part of all messages."""

    @classmethod
    def _get_test_string(cls):
        # This string is copied directly from one received from IB.
        # It serves as a format example for testing purposes only and isn't used in normal operation
        return b'{"server_id":"q0","conidEx":"495512572","conid":495512572,"_updated":1678284754734,"6119":"q0","31":"3989.50","6509":"RB","topic":"smd+495512572"}'

    @classmethod
    def create_dict_from_raw_msg(cls, raw_msg: str = None):
        """Create a system tick message from a raw json string received from IB."""
        # Dictionary from IB message
        ib_dict: dict = None
        # Translated dictionary
        new_dict: dict = {}

        if raw_msg is None:
            raise ValueError("Payload string cannot NoneType")
            return None

        ib_dict = json.loads(raw_msg)

        # The following is used to:
        # 1) Make sure we got good data from IB (i.e: the fields we care about are present)
        # 2) Map any 'odd' fields to how we want to present them (i.e: _updated->time)
        if IBFieldMapper.Topic not in ib_dict.keys():
            raise ValueError("Missing: 'topic' key!")

        # IB timestamp field is "_updated"
        if IBFieldMapper.Time in ib_dict.keys():
            new_dict[IBFieldMapper.Time] = ib_dict[IBFieldMapper.Time]
        else:
            raise ValueError("Missing: '_updated' (utc timestamp) key!")

        # Return this pre-filled in tuple for use by other message types
        return new_dict, ib_dict
