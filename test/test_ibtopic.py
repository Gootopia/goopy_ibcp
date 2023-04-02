import pytest
from goopy_ibcp.ibmsg_topic import IBTopic


class Test_IBTopic:
    """Test class for topic processing."""

    # dict of functions to process various topics
    testhandlers: dict = {}

    # Boolean flag to check if method was called...easier than patching
    _testhandler_called: bool

    # This is what the handler receives.
    _testhandler_param1: str

    # Some garbage return info...we just need to be able to identify it
    _testhander_retval: str = "topic_processed"

    # Garbage string data...just need to make sure these get passed in
    _testhandler_json_string: str = "{'key':'value'}"

    @classmethod
    def _testhandler(cls, json_msg: str):
        """Test stub for a topic handler. Easier than using patch."""
        cls._testhandler_called = True
        cls._testhandler_param1 = json_msg
        return cls._testhander_retval

    @classmethod
    def _reset_testhandlers(cls):
        """Helper function to make sure handlers are "fresh" for each test."""
        cls.testhandlers = {}
        cls._testhandler_called = False
        cls._testhandler_param1 = None

    def test_topic_strings(self):
        """Sanity check to make sure we are using proper strings."""
        assert IBTopic.MarketData == "smd"
        assert IBTopic.System == "system"
        assert IBTopic.Bulletin == "blt"

    def test_process_topic_none(self):
        """Error check the topic string can't be None."""
        with pytest.raises(ValueError):
            IBTopic.process_topic(None)

    def test_process_topic_no_handlers(self):
        """Error check that a handler dictionary can't be None."""
        with pytest.raises(ValueError):
            IBTopic.process_topic(topic="dummy", handlers=None)

    def test_process_topic_no_msg_str(self):
        """Error check that JSON message can't be None."""
        with pytest.raises(ValueError):
            # Don't care about topic or handlers...just can't be None while we test the JSON string is not None
            IBTopic.process_topic(topic="dummy", handlers={})

    def test_topic_handler(self):
        """Check that a topic can be processed if an appropriate handler is present."""
        # Good practice just to clear out the handlers prior to use.
        Test_IBTopic._reset_testhandlers()

        # Topic is unimportant...just need something that will get handled
        # String content is also un-important as we just want to make sure it gets passed to handler
        self.testhandlers[IBTopic.MarketData] = Test_IBTopic._testhandler

        test_topic = "smd+1234"
        retval = IBTopic.process_topic(
            topic=test_topic,
            handlers=self.testhandlers,
            json_msg=self._testhandler_json_string,
        )

        # Check that handler was called
        assert Test_IBTopic._testhandler_called == True

        # Check that handler received proper parameters in the proper order
        assert Test_IBTopic._testhandler_param1 == self._testhandler_json_string

        # Also verify we returned what it wanted us to get
        assert retval == Test_IBTopic._testhander_retval

    def test_topic_not_handled(self):
        """Check that we do nothing if no topic handler is available."""
        # Good practice just to clear out the handlers prior to use.
        Test_IBTopic._reset_testhandlers()

        # Handler and data don't matter...it shouldn't get called anyway
        self.testhandlers[IBTopic.MarketData] = Test_IBTopic._testhandler
        retval = IBTopic.process_topic(
            topic="no-process",
            handlers=self.testhandlers,
            json_msg=Test_IBTopic._testhandler_json_string,
        )

        # Handler shouldn't get called
        assert Test_IBTopic._testhandler_called == False

        # So return value should be default 'None'
        assert retval is None
