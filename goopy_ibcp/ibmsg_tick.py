"""IB Message: Tick.

New tick received from quote server.
"""
from goopy_ibcp.jsonpacket import JSONPacket
from goopy_ibcp.ibmsg_topic import IBTopic
from enum import Enum


class IBMsgTick(JSONPacket):
    """New tick received from IB quote server."""

    class Fields:
        """Fields used by tick message."""

        Time: str = "time"
        Conid: str = "conid"
        Price: str = "price"

    class TickTypes:
        """Types of tick data available."""

        Bid: str = "bid"
        Ask: str = "ask"
        Last: str = "last"

    def __init__(self, payload: dict, ticktype: TickTypes) -> None:
        conid = payload[IBMsgTick.Fields.Conid]
        # allows topics to be made more specific so that additional filtering can be done by ZMQ
        tick_topic = f"{IBTopic.Tick}_{conid}_{ticktype}"
        super().__init__(tick_topic, payload)

    @staticmethod
    def payload_dict(timestamp_utc: str, conid: str, price: str):
        """Build payload dictionary."""
        payload = {}
        payload[IBMsgTick.Fields.Time] = timestamp_utc
        payload[IBMsgTick.Fields.Conid] = conid
        payload[IBMsgTick.Fields.Price] = price
        return payload
