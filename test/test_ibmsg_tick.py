from goopy_ibcp.ibmsg_topic import IBTopic
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

    def test_topic_last(self):
        """Check for correct topic: Last"""
        test_payload = Test_IBMsgTick.get_test_payload()
        msg = IBMsgTick(test_payload, IBMsgTick.TickTypes.Last)
        topic = f"{IBTopic.Tick}_{Test_IBMsgTick.conid}_{IBMsgTick.TickTypes.Last}"
        assert msg.topic == topic

    def test_topic_bid(self):
        """Check for topic: Bid"""
        test_payload = Test_IBMsgTick.get_test_payload()
        msg = IBMsgTick(test_payload, IBMsgTick.TickTypes.Bid)
        topic = f"{IBTopic.Tick}_{Test_IBMsgTick.conid}_{IBMsgTick.TickTypes.Bid}"
        assert msg.topic == topic

    def test_topic_ask(self):
        """Check for topic: Ask"""
        test_payload = Test_IBMsgTick.get_test_payload()
        msg = IBMsgTick(test_payload, IBMsgTick.TickTypes.Ask)
        topic = f"{IBTopic.Tick}_{Test_IBMsgTick.conid}_{IBMsgTick.TickTypes.Ask}"
        assert msg.topic == topic

    def test_payload_decoder(self):
        """Check the build payload function."""
        test_payload = Test_IBMsgTick.get_test_payload()
        msg_tick = IBMsgTick(test_payload, IBMsgTick.TickTypes.Last)
        pkt = msg_tick.build_packet()
        decoded = msg_tick.get_packet_payload(pkt)
        assert decoded[IBMsgTick.Fields.Conid] == Test_IBMsgTick.conid
        assert decoded[IBMsgTick.Fields.Price] == Test_IBMsgTick.price
        assert decoded[IBMsgTick.Fields.Time] == Test_IBMsgTick.utc_timestamp
