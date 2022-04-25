#!/usr/bin/env python

import sys, os

import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage



class MsgProcessor:
    def __init__(self):
        self.counter = 0

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        """
        An asynchronous counting message handler.
        """
        self.counter += 1
        if self.counter % 10000 == 0:
            print(f' [x] Received {self.counter} messages.')

async def receive_requests() -> None:
    # Perform connection
    connection = await connect('amqp://rabbitmq:rabbitmq@rabbitmq_inst/')
    # Set up a dict with a counter
    mp = MsgProcessor()
    # Init connection and receive messages
    async with connection:
        # Creating a channel
        channel = await connection.channel()
        # Declaring queue
        queue = await channel.declare_queue('hello')
        # Start listening the queue with name 'hello'
        await queue.consume(mp.on_message, no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C.')
        await asyncio.Future()

async def initial_wait() -> None:
    """
    Sleep for the amount of seconds taken from the environment variables
    """
    await asyncio.sleep(
        float(os.environ.get('START_WAIT_S', 5))
    )

async def main() -> None:
    """
    Wait for an interval set in env variables and process the messages after.
    """
    await initial_wait()
    await receive_requests()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
