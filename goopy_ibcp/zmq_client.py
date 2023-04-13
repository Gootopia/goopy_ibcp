"""zmq message client."""
import zmq
from loguru import logger


class ZmqClient:
    """zmq client."""

    def __init__(self):
        """Our constructor."""
        self.context = zmq.Context()
        self.poller = zmq.Poller()

        # Dictionary of all sockets this client connects to
        self.sockets = {}

    def register_msg_subscription(self, socket_name: str, msg: str):
        """Subscribe to a message on a given named socket."""
        if socket_name in self.sockets.keys():
            socket = self.sockets[socket_name]
            socket.setsockopt_string(zmq.SUBSCRIBE, msg)

    def add_socket(self, name: str, address="tcp://*:5555"):
        """Add a new socket to the client."""
        new_socket = self.context.socket(zmq.SUB)
        new_socket.connect(f"{address}")
        self.poller.register(new_socket, zmq.POLLIN)
        self.sockets[name] = new_socket
