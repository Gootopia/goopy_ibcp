"""IB Message: Tick."""
from ibmsg import IBMsgConverter
from ibmsg_topic import IBTopic
from ibfieldmapper import IBFieldMapper


class IBMsgConverterTick(IBMsgConverter):
    """Extract desired fields from IB tick messages for system tick messages."""

    # There's lots of keys in an IB message dict, but we only need to re-transmit a portion of them
    required_keys: list = [IBFieldMapper.Conid, IBFieldMapper.Time, IBFieldMapper.Topic]

    @classmethod
    def _get_test_tick_string(cls):
        # This string is copied directly from one received from IB.
        # It serves as a format example for testing purposes only and isn't used in normal operation
        return b'{"server_id":"q0","conidEx":"495512572","conid":495512572,"_updated":1678666665031,"6119":"q0","84":"3913.25","31":"3913.50","86":"3913.75","6509":"RB","topic":"smd+495512572"}'

    @classmethod
    def verify_keys(cls, msg_dict: dict) -> list:
        """Check that required keys are present in the message dictionary."""
        missing_keys = cls._check_keys(msg_dict, cls.required_keys)
        return missing_keys

    @classmethod
    def create_dict_from_raw_msg(cls, raw_msg: str = None) -> dict:
        """Create a system tick message from a raw json string received from IB."""
        # The call to super() does the string conversion and gives us the starting msg dict.
        ib_msg_dict = super().create_dict_from_raw_msg(raw_msg)
        transmit_msg_dict = {}

        # Verify that all the keys that we care about are present in this message
        missing_keys = cls.verify_keys(ib_msg_dict)

        # Once required keys are verifed, manually check for price data
        # We can have more than one (depending on market data subscription), but we need at least one.
        if not missing_keys:
            transmit_msg_dict[IBFieldMapper.Conid] = ib_msg_dict[IBFieldMapper.Conid]
            transmit_msg_dict[IBFieldMapper.Time] = ib_msg_dict[IBFieldMapper.Time]
            transmit_msg_dict[IBFieldMapper.Topic] = ib_msg_dict[IBFieldMapper.Topic]

            # Price data (There are potentially lots). We only care about some of them.
            foundPriceData = False
            if IBFieldMapper.Price_Last in ib_msg_dict.keys():
                transmit_msg_dict[IBFieldMapper.Price_Last] = ib_msg_dict[
                    IBFieldMapper.Price_Last
                ]
                foundPriceData = True

            if IBFieldMapper.Price_Ask in ib_msg_dict.keys():
                transmit_msg_dict[IBFieldMapper.Price_Ask] = ib_msg_dict[
                    IBFieldMapper.Price_Ask
                ]
                foundPriceData = True

            if IBFieldMapper.Price_Bid in ib_msg_dict.keys():
                transmit_msg_dict[IBFieldMapper.Price_Bid] = ib_msg_dict[
                    IBFieldMapper.Price_Bid
                ]
                foundPriceData = True

            if foundPriceData is False:
                raise ValueError("Missing: price data!")

        return transmit_msg_dict
