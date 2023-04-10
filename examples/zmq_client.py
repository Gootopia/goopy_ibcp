# Example ZeroMQ client example with ZMQ polling
# Polling is used to check for the receipt of various topics (see ZMQ docs)
# IB Server publishes tick messages with topic 'smd+{conid}

import zmq
from time import sleep
from loguru import logger

connection = "tcp://localhost:5555"
# message topic to subscribe to
msg_subscription = "smd"
# Amount of time to wait for a message be it's flagged
timeout_ms = 30000


def thread():
    context = zmq.Context()
    logger.log("DEBUG", f"Created socket")
    socket_es = context.socket(zmq.SUB)
    socket_es.connect(f"{connection}")
    logger.log("DEBUG", f"Connecting to '{connection}'")
    socket_es.setsockopt_string(zmq.SUBSCRIBE, f"{msg_subscription}")
    logger.log("DEBUG", f"Subscribing to: '{msg_subscription}'")
    poller = zmq.Poller()
    poller.register(socket_es, zmq.POLLIN)

    logger.log("DEBUG", f"Entering polling loop")
    msg = None
    while True:
        try:
            sock = dict(poller.poll(timeout_ms))
        except KeyboardInterrupt:
            logger.log("DEBUG", f"Polling terminated via Ctrl-C")
            break
        except Exception as e:
            logger.log("DEBUG", f"Exception {e}")

        if sock is not None:
            if socket_es in sock:
                msg = socket_es.recv_string()
                logger.log("DEBUG", f"Received {msg}")

        sleep(0.001)

    logger.log("DEBUG", f"Exited polling loop")


if __name__ == "__main__":
    thread()
