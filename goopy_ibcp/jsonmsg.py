"""Message formatter for JSON message packets.
For convenience, we are assuming a "pub/sub" style message where clients "subscribe"
to various types of messages ("topics").
We are also assuming zeromq as the messaging library

"""
from abc import ABC
import json


class JSONMsg(ABC):
    """Template base class for transmitting messages."""

    def __init__(self, topic: str = "", separator: str = "&&") -> None:
        """JSON Message constructor."""
        if (topic == "") or (topic is None):
            raise ValueError("Topic cannot be empty string or None.")

        self.topic = topic
        self.separator = separator
        super().__init__()

    @staticmethod
    def format_payload(payload: dict = None):
        """Convert payload dictionary into transmit string (json)."""
        if payload is None:
            raise ValueError("Payload cannot be None")

        payload_formatted = json.dumps(payload)
        return payload_formatted

    def build_message(self, payload: dict = None):
        """Transmit message format is {topic}{separator}{payload_json}."""
        payload_str = JSONMsg.format_payload(payload)

        msg_str = f"{self.topic}{self.separator}{payload_str}"
        return msg_str
