# Example PyZmq client
# Refer to event loops: https://pyzmq.readthedocs.io/en/latest/howto/eventloop.html#

import zmq.eventloop as ze
from zmq.eventloop.zmqstream import ZMQStream

from time import sleep
from loguru import logger
from goopy_ibcp.zmq_client import ZmqClient
from goopy_ibcp.ibmsg_topic import IBTopic

# Socket connection
connection_ib = "tcp://localhost:5555"
# Socket name
socket_name_ib = "interactive_brokers"


def recv_callback(msg):
    """This Handler method called every time something is received."""
    print(f"message={msg}")


def msg_client():
    """PyZMQ client to:
    1) Create a socket
    2) Register a listener and a handler
    3) Create a listening loop
    """
    ZmqClient.log_version()
    # IB Server publishes tick messages with topic 'smd+{conid}, but for the example just set filter to subscribe to everything
    ZmqClient.register_listener_stream(
        socket_name_ib, connection_ib, IBTopic.MarketData, recv_callback
    )
    ze.IOLoop.instance().start()

    # Normally don't get here without user exit or error
    logger.log("DEBUG", f"Exited polling loop")


if __name__ == "__main__":
    msg_client()
