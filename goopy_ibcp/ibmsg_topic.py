from goopy_ibcp.jsonpacket import JSONPacket


class IBTopic:
    """Allowed topic categories in IB.
    Topics are the message prefixes transmitted in network payloads.
    These enable filtering of message traffic via the ZMQ framework by cateory or more"""

    Tick: str = "tick"
