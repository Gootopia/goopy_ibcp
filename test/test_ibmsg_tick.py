import json

from goopy_ibcp.ibmsg_topics import IBTopics
from goopy_ibcp.ibmsg_tick import IBMsgTick
from datetime import datetime, timezone


class Test_IBMsgTick:
    """Test class for Tick Messages.
    Includes the following:
    time=UTC timestamp
    conid=IB symbol conid
    price=Price value
    type=bid,ask,last (as appropriate)
    """

    conid: str = "495512572"
    price: str = "2000.00"
    utc_timestamp = None

    @classmethod
    def get_test_payload(cls):
        """Initialize a test payload."""
        dt = datetime(1987, 10, 19, 9, 30)
        utc_time = dt.replace(tzinfo=timezone.utc)
        # Timestamps from IB are in UTC, so we'll keep that format
        cls.utc_timestamp = utc_time.timestamp()
        return IBMsgTick.payload_dict(cls.utc_timestamp, cls.conid, cls.price)

    def test_topic(self):
        """Check for correct topic."""
        test_payload = Test_IBMsgTick.get_test_payload()
        msg = IBMsgTick(test_payload)
        topic = f"{IBTopics.tick.name}_{Test_IBMsgTick.conid}"
        assert msg.topic == topic

    def test_payload_decoder(self):
        """Check the build payload function."""
        test_payload = Test_IBMsgTick.get_test_payload()
        msg_tick = IBMsgTick(test_payload)
        pkt = msg_tick.build_packet()
        decoded = msg_tick.get_packet_payload(pkt)
        assert msg_tick.getdata(decoded, IBMsgTick.Fields.conid) == Test_IBMsgTick.conid
        assert msg_tick.getdata(decoded, IBMsgTick.Fields.price) == Test_IBMsgTick.price
        assert (
            msg_tick.getdata(decoded, IBMsgTick.Fields.time)
            == Test_IBMsgTick.utc_timestamp
        )
