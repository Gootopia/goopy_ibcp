"""zmq message client."""
import zmq
import zmq.asyncio
from loguru import logger


class ZmqClient:
    """ZMQ Client for connecting to one or more sockets."""

    # pyzmq async context. Only contexts are thread safe, so use one for all classes in a process
    global_context: zmq.asyncio.Context = zmq.asyncio.Context.instance()
    sockets: dict = {}
    logging: bool = True

    @staticmethod
    def log_version():
        """Get some info about the zmq/pyzmq versions that are being used."""
        zmq_version = zmq.zmq_version()
        pyzmq_version = zmq.pyzmq_version()
        log_msg = f"ZMQClient (zmq,pyzmq)=({zmq_version},{pyzmq_version})"
        logger.log("DEBUG", log_msg)
        return (zmq_version, pyzmq_version)

    @classmethod
    def register_listener(cls, socket_name: str, msg: str):
        """Subscribe to a message on a given named socket."""
        if socket_name in cls.sockets.keys():
            socket = cls.sockets[socket_name]
            socket.setsockopt_string(zmq.SUBSCRIBE, msg)
            log_msg = f"New message subscriber '{msg}' on socket '{socket_name}'"
            logger.log("DEBUG", log_msg)
        else:
            raise KeyError(f"No socket named: '{socket_name}'")

    @classmethod
    def add_socket(cls, name: str, address="tcp://*:5555"):
        """Add a new socket to the client test2."""
        new_socket = cls.global_context.socket(zmq.SUB)
        new_socket.connect(address)
        log_msg = f"New socket '{name}' with address '{address}'"
        logger.log("DEBUG", log_msg)

        cls.sockets[name] = new_socket
        return new_socket
