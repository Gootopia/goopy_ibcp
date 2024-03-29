import pytest
from goopy_ibcp.zmq_publisher import ZmqPublisher


class TestZmqPublisher:
    def test_empty_message(self):
        """Message can't be empty"""
        assert ZmqPublisher.check_msg_format(None) is False

    def test_not_string(self):
        """Only strings are valid"""
        assert ZmqPublisher.check_msg_format(0) is False
