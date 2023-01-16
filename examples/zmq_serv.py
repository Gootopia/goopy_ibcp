#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
from datetime import datetime
from random import randrange
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
tick_last = 0
while True:
    tick_time = datetime.now()
    tick_symbol = "es"
    # tick_last = randrange(3000, 3500)
    tick_last = tick_last + 1
    result = socket.send_string(f"{tick_symbol},{tick_time},{tick_last}")
    print(f"{tick_time}:{tick_symbol}={tick_last} (Result={result})")
    sleep(0.01)
