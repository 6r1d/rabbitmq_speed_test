#!/usr/bin/env python

import pika, sys, os
from time import sleep

START_WAIT = 4

def main():
    sleep(START_WAIT)

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

    def callback(ch, method, properties, body):
        # print(f' [x] Received {len(body)}.')
        pass

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C\n')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
