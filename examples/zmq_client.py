# ZeroMQ client example with ZMQ polling
# Polling is used to check for the receipt of various topics (see ZMQ docs)

import zmq
from time import sleep
from loguru import logger

connection = "tcp://localhost:5555"
msg_subscription = "smd"


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
    while True:
        try:
            sock = dict(poller.poll(5000))
        except KeyboardInterrupt:
            break

        msg = None

        if socket_es in sock:
            msg = socket_es.recv_string()
            logger.log("DEBUG", f"Received {msg}")

        sleep(0.001)

    logger.log("DEBUG", f"Exited polling loop")


if __name__ == "__main__":
    thread()
