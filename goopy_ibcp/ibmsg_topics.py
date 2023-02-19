from goopy_ibcp.jsonpacket import JSONPacket
from enum import Enum


class IBTopics(Enum):
    """Allowed topic categories in IB."""

    tick = 0
