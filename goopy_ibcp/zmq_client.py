"""zmq message client."""
import zmq
from loguru import logger


class ZmqClient:
    """ZMQ Client for connecting to one or more sockets."""

    def __init__(self, logger_on: bool = True):
        """Our constructor."""
        self.context = zmq.Context()
        self.poller = zmq.Poller()

        # When true, relevant information will be logged
        self.logging = logger_on

        # Dictionary of all sockets this client connects to
        self.sockets = {}
        logger.log(
            "DEBUG",
            f"New ZMQ Client (zmq,pyzmq)=({zmq.zmq_version()},{zmq.pyzmq_version()})",
        )

    def register_socket_msg_listener(self, socket_name: str, msg: str):
        """Subscribe to a message on a given named socket."""
        if socket_name in self.sockets.keys():
            socket = self.sockets[socket_name]
            socket.setsockopt_string(zmq.SUBSCRIBE, msg)
            logger.log(
                "DEBUG",
                f"New message subscriber '{msg}' on socket '{socket_name}'",
            )
        else:
            raise KeyError(f"No socket named: '{socket_name}'")

    def add_socket(self, name: str, address="tcp://*:5555"):
        """Add a new socket to the client."""
        new_socket = self.context.socket(zmq.SUB)
        new_socket.connect(f"{address}")
        logger.log("DEBUG", f"New socket '{name}' with address '{address}'")

        self.poller.register(new_socket, zmq.POLLIN)
        self.sockets[name] = new_socket
