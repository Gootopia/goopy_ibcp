"""IB Message.

Base message from which other messages are derived.
"""
from abc import ABC, abstractclassmethod
from goopy_ibcp.ibfieldmapper import IBFieldMapper
from goopy_ibcp.jsonpacket import JSONPacket
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


class IBMsgConverter(ABC):
    """Abstract base class for defining system messages."""

    @classmethod
    def _get_test_tick_string(cls):
        # This string is copied directly from one received from IB.
        # It serves as a format example for testing purposes only and isn't used in normal operation
        return b'{"server_id":"q0","conidEx":"495512572","conid":495512572,"_updated":1678284754734,"6119":"q0","31":"3989.50","6509":"RB","topic":"smd+495512572"}'

    @classmethod
    def _get_test_dict(cls, json_str: str) -> dict:
        """Helper function to create a dict when given a proper json message."""
        if json_str is None:
            raise ValueError("JSON string cannot be none.")

        test_dict = json.loads(json_str)
        return test_dict

    @classmethod
    def _check_keys(cls, msg_dict: dict, required_keys: list = None) -> list:
        """Verify the presence of a specific set of keys in a dictionary."""
        missing_keys = []

        if required_keys is not None:
            for verify_key in required_keys:
                if verify_key not in msg_dict.keys():
                    missing_keys.append(verify_key)

        return missing_keys

    @abstractclassmethod
    def verify_keys(cls, keys: list) -> list:
        """Placeholder function for checking for a specific list of keys. Overridden for actual messages."""
        pass

    @classmethod
    def verify_msg_topic(
        cls, msg_dict: dict, match_topic: str, exact_match: bool = True
    ) -> bool:
        """Verify that the topic in a message string matches a desired topic (either exact or as sub-string)."""
        if IBFieldMapper.Topic in msg_dict.keys():
            topic: str = msg_dict[IBFieldMapper.Topic]

            if exact_match is False:
                match_topic_is_substring = match_topic in topic
                return match_topic_is_substring

            else:
                match_topic_is_exact = match_topic == topic
                return match_topic_is_exact

    @classmethod
    def create_dict_from_raw_msg(cls, raw_msg: str = None):
        """Create a system tick message from a raw json string received from IB."""
        # Dictionary from IB message
        ib_msg_dict: dict = None

        if raw_msg is None:
            raise ValueError("Payload string cannot NoneType")
            return None
        try:
            ib_msg_dict = json.loads(raw_msg)

        # TODO: make this a bit more defensive. For now we just want to see what exceptions we might raise
        # so we can handle them more explicitly
        except Exception as e:
            raise e

        # Return both dict for use by other message types
        return ib_msg_dict
