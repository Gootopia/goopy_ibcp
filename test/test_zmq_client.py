import pytest

from goopy_ibcp.zmq_client import ZmqClient


class Test_ZmqClient:
    def test_register_listener(self):
        test_client = ZmqClient()

        with pytest.raises(KeyError):
            test_client.register_listener("bad_socket_name", "message")
