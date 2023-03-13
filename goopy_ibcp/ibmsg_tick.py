"""IB Message: Tick."""
from goopy_ibcp.ibmsg import IBMsg, IBMsgConverter
from goopy_ibcp.ibmsg_topic import IBTopic
from goopy_ibcp.ibfieldmapper import IBFieldMapper
import json


class IBMsgTick(IBMsg):
    """System message for tick data received from IB quote server."""

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
        """Constructor."""
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


class IBMsgConverterTick(IBMsgConverter):
    """Extract desired fields from IB tick messages for system tick messages."""

    @classmethod
    def _get_test_string(cls):
        # This string is copied directly from one received from IB.
        # It serves as a format example for testing purposes only and isn't used in normal operation
        return b'{"server_id":"q0","conidEx":"495512572","conid":495512572,"_updated":1678666665031,"6119":"q0","84":"3913.25","31":"3913.50","86":"3913.75","6509":"RB","topic":"smd+495512572"}'

    @classmethod
    def create_dict_from_raw_msg(cls, raw_msg: str = None):
        """Create a system tick message from a raw json string received from IB."""
        new_dict, ib_dict = super().create_dict_from_raw_msg(raw_msg)

        # Contract identifier
        if IBFieldMapper.Conid in ib_dict.keys():
            new_dict[IBFieldMapper.Conid] = ib_dict[IBFieldMapper.Conid]
        else:
            raise ValueError("Missing: 'conid' (contract id) key!")

        foundPriceData = False

        # Price data (There are potentially lots). We only care about some of them.
        if IBFieldMapper.Price_Last in ib_dict.keys():
            new_dict[IBFieldMapper.Price_Last] = ib_dict[IBFieldMapper.Price_Last]
            foundPriceData = True

        if IBFieldMapper.Price_Ask in ib_dict.keys():
            new_dict[IBFieldMapper.Price_Ask] = ib_dict[IBFieldMapper.Price_Ask]
            foundPriceData = True

        if IBFieldMapper.Price_Bid in ib_dict.keys():
            new_dict[IBFieldMapper.Price_Bid] = ib_dict[IBFieldMapper.Price_Bid]
            foundPriceData = True

        if foundPriceData is False:
            raise ValueError("Missing: price data!")

        return new_dict
