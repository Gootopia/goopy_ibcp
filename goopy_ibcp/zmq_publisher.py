"""zmq message publisher."""

import zmq
from datetime import datetime


class ZmqPublisher:
    """zmq publisher."""

    context = None

    def __init__(self, binding="tcp://*:5555"):
        self.context = zmq.Context()
        self.binding = binding
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(binding)
        self.tick_last = 0

    def publish(self, msg):
        tick_time = datetime.now()
        xmit_msg = f"{tick_time}"
        result = self.socket.send_string(msg)
        # print(f"{tick_time}:{tick_symbol}={self.tick_last} (Result={result})")
