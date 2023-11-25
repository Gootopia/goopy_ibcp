from loguru import logger
import asyncio
import time
import subprocess

from zmq_publisher import ZmqPublisher


async def short_running_process():
    print("Start Short Running")
    for i in range(1, 10):
        logger.log("DEBUG", f"Side Process: {i}")
        await asyncio.sleep(5)


async def start_process():
    print("Starting Stuff")
    methods = [
        short_running_process(),
    ]
    # pass in desired list as arguments
    await asyncio.gather(*methods)


async def create_background():
    asyncio.create_subprocess_shell(start_process())


def counter():
    for n in range(100):
        print(f"N={n}")
        time.sleep(5)


if __name__ == "__main__":
    # asyncio.run(create_background())
    # time.sleep(30)

    print("Hello")
    counter()
