"""Message formatter for JSON message packets.
For convenience, we are assuming a "pub/sub" style message where clients "subscribe"
to various types of messages ("topics").
We are also assuming zeromq as the messaging library

"""
from abc import ABC
from enum import Enum
import json


class JSONPacket(ABC):
    """Template base class for transmitting messages."""

    # Used to separate the topic from the payload
    PacketSeparator: str = "+"
    # Optional suffix on a topic to allow more specific messages of a given topic type
    TopicSeparator: str = "_"

    def __init__(
        self, topic: str = "", payload: dict = None, separator: str = PacketSeparator
    ) -> None:
        """JSON Message constructor."""
        if (topic == "") or (topic is None):
            raise ValueError("Topic cannot be empty string or None.")

        self.topic = topic
        self.separator = separator
        self.payload = payload
        super().__init__()

    @staticmethod
    def format_payload(payload: dict = None):
        """Convert payload dictionary into transmit string (json)."""
        if payload is None:
            payload = {}

        payload_formatted = json.dumps(payload)
        return payload_formatted

    @staticmethod
    def get_packet_payload(packet: str) -> dict:
        """Extract json payload from packet and convert to dict"""
        packet_json = packet.split(JSONPacket.PacketSeparator, 1)
        payload_json = packet_json[1]
        packet_dict = json.loads(payload_json)
        return packet_dict

    def build_packet(self):
        """Packet format is {topic}{separator}{payload_json}."""
        formatted_msg = JSONPacket.format_payload(self.payload)
        packet = f"{self.topic}{self.separator}{formatted_msg}"
        self.formatted_packet = packet
        return packet
