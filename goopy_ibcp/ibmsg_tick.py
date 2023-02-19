"""IB Message: Tick.

New tick received from quote server.
"""
from goopy_ibcp.jsonpacket import JSONPacket
from goopy_ibcp.ibmsg_topics import IBTopics
from enum import Enum

# - Receive JSON message from IB Server
# - convert to dict
# - extract desired fields
# - convert to dict
# - build payload for ZMQ


class IBMsgTick(JSONPacket):
    """New tick received from IB quote server."""

    class Fields(Enum):
        """Fields used by tick message."""

        time = 0
        conid = 1
        price = 2

    def __init__(self, payload: dict) -> None:
        conid = self.getdata(payload, IBMsgTick.Fields.conid)
        # allows topics to be made more specific so that additional filtering can be done by ZMQ
        tick_topic = f"{IBTopics.tick.name}_{conid}"
        super().__init__(tick_topic, payload)

    @staticmethod
    def payload_dict(timestamp_utc: str, conid: str, price: str):
        """Build payload dictionary."""
        payload = {}
        payload[IBMsgTick.Fields.time.name] = timestamp_utc
        payload[IBMsgTick.Fields.conid.name] = conid
        payload[IBMsgTick.Fields.price.name] = price
        return payload
