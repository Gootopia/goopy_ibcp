# Example ZeroMQ client example with ZMQ polling
# Polling is used to check for the receipt of various topics (see ZMQ docs)
# IB Server publishes tick messages with topic 'smd+{conid}

import zmq
from time import sleep
from loguru import logger
from goopy_ibcp.zmq_client import ZmqClient

connection = "tcp://localhost:5555"
# message topic to subscribe to
msg_subscription = "smd"

socket_tickfeed = "ticks"

# Amount of time to wait for a message
timeout_ms = 30000


def ib_client_thread():
    """Client thread for handling IB message traffic."""

    client = ZmqClient()
    logger.log("DEBUG", f"Opening socket to {connection}")
    client.add_socket(socket_tickfeed, connection)

    client.register_msg_subscription(socket_tickfeed, msg_subscription)
    logger.log("DEBUG", f"Registering msg '{msg_subscription}'")

    logger.log("DEBUG", f"Entering polling loop")
    msg = None

    while True:
        try:
            socket_with_msg = dict(client.poller.poll(timeout_ms))
        except KeyboardInterrupt:
            logger.log("DEBUG", f"Polling terminated via Ctrl-C")
            break
        except Exception as e:
            logger.log("DEBUG", f"Exception {e}")

        if socket_with_msg is not None:
            for socket_name in client.sockets:
                socket = client.sockets[socket_name]
                if socket in socket_with_msg:
                    msg = socket.recv_string()
                    logger.log("DEBUG", f"Received {msg}")

        sleep(0.001)

    # Normally don't get here without user exit or error
    logger.log("DEBUG", f"Exited polling loop")


if __name__ == "__main__":
    ib_client_thread()
