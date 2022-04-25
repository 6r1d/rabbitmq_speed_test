#!/usr/bin/env python

import pika, sys, os
from time import sleep

def main():
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

    message_count = 0

    def callback(ch, method, properties, body):
        nonlocal message_count
        message_count += 1
        if message_count % 10000 == 0:
            print(f' [x] Received {message_count} messages.')

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C\n')
    channel.start_consuming()

def initial_wait():
    """
    Sleep for the amount of seconds taken from the environment variables
    """
    sleep(
        float(os.environ.get('START_WAIT_S', 5))
    )

if __name__ == '__main__':
    try:
        initial_wait()
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
