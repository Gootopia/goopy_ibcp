import pytest
from unittest.mock import patch

from goopy_ibcp.zmq_publisher import ZmqPublisher

# @patch('goopy_ibcp.clientportal_websockets.Certificate.get_certificate')
class TestZmqPublisher:
    def test_empty_message(self):
        """Message can't be empty"""
        assert ZmqPublisher.check_msg_format(None) is False

    def test_not_string(self):
        """Only strings are valid"""
        assert ZmqPublisher.check_msg_format(0) is False
