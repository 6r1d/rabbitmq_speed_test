#!/usr/bin/env python

import pika
from os import environ
from time import sleep
from hs_gen.gen import ParagraphGenerator

START_WAIT_S = float(environ.get('START_WAIT_S', 5))
DELAY_S = float(environ.get('MSG_DELAY_S', 1))

def main():
    # Init the paragraph generator while
    # passing Docker-compose environment variables
    gen = ParagraphGenerator(
        min_sentence_length=int(environ.get('MIN_SENTENCE_LENGTH'), 10),
        max_sentence_length=int(environ.get('MAX_SENTENCE_LENGTH'), 10),
        min_sentences=int(environ.get('MIN_SENTENCES'), 10),
        max_sentences=int(environ.get('MAX_SENTENCES'), 10)
    )
    # Establish the RabbitMQ connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            'rabbitmq_inst',
            5672,
            '/',
            pika.PlainCredentials('rabbitmq', 'rabbitmq')
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    print(' [*] Starting the message generator. To exit press CTRL+C\n')

    while True:
        paragraph = gen.generate_paragraph()
        channel.basic_publish(
            exchange='', routing_key='hello', body=paragraph
        )
        # print(f' [x] Sent {len(paragraph)}.')
        if DELAY_S:
            sleep(DELAY_S)

    connection.close()

if __name__ == '__main__':
    try:
        sleep(START_WAIT_S)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
