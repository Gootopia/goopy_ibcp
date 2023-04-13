"""zmq message publisher."""
import zmq


class ZmqPublisher:
    """zmq publisher.
    Requirements:
    1) Format is "topic&&{json_msg}"
    2) Payloads cannot be empty
    """

    def __init__(self, binding="tcp://*:5555"):
        """Our constructor."""
        self.context = zmq.Context()
        self.binding = binding
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(binding)

    @staticmethod
    def check_msg_format(msg):
        """Pre-check prior to transmission."""
        if msg is None:
            return False

        # Currently we are only using human readable strings as payloads
        if isinstance(msg, str) is False:
            return False

        return True

    def publish_string(self, msg):
        """Transmit string via zmq socket."""
        if ZmqPublisher.check_msg_format(msg) is True:
            try:
                # TODO: Error checking of return results
                result = self.socket.send_string(msg)
            except Exception as e:
                raise e
        else:
            return False
