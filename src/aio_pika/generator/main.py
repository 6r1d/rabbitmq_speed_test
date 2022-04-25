#!/usr/bin/env python

from os import environ
from hs_gen.gen import ParagraphGenerator

import asyncio

from aio_pika import Message, connect

DELAY_S = float(environ.get('MSG_DELAY_S', 1))

async def initial_wait() -> None:
    """
    Sleep for the amount of seconds taken from the environment variables
    """
    await asyncio.sleep(
        float(environ.get('START_WAIT_S', 5))
    )

async def send_requests() -> None:
    # Init the paragraph generator while
    # passing Docker-compose environment variables
    gen = ParagraphGenerator(
        dict_path='/usr/share/hunspell/en_GB.dic',
        min_sentence_length=int(environ.get('MIN_SENTENCE_LENGTH'), 10),
        max_sentence_length=int(environ.get('MAX_SENTENCE_LENGTH'), 10),
        min_sentences=int(environ.get('MIN_SENTENCES'), 10),
        max_sentences=int(environ.get('MAX_SENTENCES'), 10)
    )
    # Perform connection
    connection = await connect("amqp://rabbitmq:rabbitmq@rabbitmq_inst/")
    # TODO describe
    print(' [*] Starting the message generator. To exit press CTRL+C\n')
    # Declare a queue for the current connection,
    # generate paragraphs, send messages
    async with connection:
        # Creating a channel
        channel = await connection.channel()
        # Declaring queue
        queue = await channel.declare_queue('hello')
        # Generate and send messages with a given delay
        while True:
            paragraph = gen.generate_paragraph()
            # Sending the message
            await channel.default_exchange.publish(
                Message(paragraph.encode('utf-8')),
                routing_key=queue.name,
            )
            if DELAY_S:
                await asyncio.sleep(DELAY_S)

async def main() -> None:
    await initial_wait()
    await send_requests()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
