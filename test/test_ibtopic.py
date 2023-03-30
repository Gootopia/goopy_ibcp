import pytest
from goopy_ibcp.ibmsg_topic import IBTopic


class Test_IBTopic:
    """Test class for topic processing."""

    # dict of functions to process various topics
    testhandlers: dict = {}

    # Boolean flag to check if method was called...easier than patching
    _testhandler_called: bool

    # Some garbage return info...we just need to be able to identify it
    _testhander_retval: str = "topic_processed"

    @classmethod
    def _testhandler(cls, topic: str):
        """Test stub for a topic handler. Easier than using patch."""
        cls._testhandler_called = True
        return cls._testhander_retval

    @classmethod
    def _reset_testhandlers(cls):
        """Helper function to make sure handlers are "fresh" for each test."""
        cls.testhandlers = {}
        cls._testhandler_called = False

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

    def test_topic_handler(self):
        """Check that a topic can be processed if an appropriate handler is present."""
        # Good practice just to clear out the handlers prior to use.
        Test_IBTopic._reset_testhandlers()

        # Topic is unimportant...just need something that will get handled
        self.testhandlers[IBTopic.MarketData] = Test_IBTopic._testhandler
        retval = IBTopic.process_topic(topic="smd+1234", handlers=self.testhandlers)

        # Check that handler was called
        assert Test_IBTopic._testhandler_called == True
        # Also verify we returned what it wanted us to get
        assert retval == Test_IBTopic._testhander_retval

    def test_topic_not_handled(self):
        """Check that we do nothing if no topic handler is available."""
        # Good practice just to clear out the handlers prior to use.
        Test_IBTopic._reset_testhandlers()

        # Handler doesn't matter...just make sure we have a valid one which won't get called.
        self.testhandlers[IBTopic.MarketData] = Test_IBTopic._testhandler
        retval = IBTopic.process_topic(topic="no-process", handlers=self.testhandlers)

        # Handler shouldn't get called
        assert Test_IBTopic._testhandler_called == False
        # So return value should be default 'None'
        assert retval is None
