#!/usr/bin/env python

import pika
from os import environ
from time import sleep
from string import ascii_letters
from random import choice, randint

START_WAIT_S = float(environ.get('START_WAIT_S', 5))
DELAY_S = float(environ.get('MSG_DELAY_S', 1))
DICT_PATH = '/usr/share/hunspell/en_GB-large.dic'

def get_dictionary():
    dict_words = []
    with open(DICT_PATH, 'r') as dict_file:
        dict_words = list(
            filter(
                lambda word: not bool(set(word) - set(ascii_letters)),
                [line.strip().split('/')[0] for line in dict_file.readlines()]
            )
        )
    return (
        list(filter(lambda word: word[0].islower(), dict_words)),
        list(filter(lambda word: word[0].isupper(), dict_words))
    )

def generate_sentence(normal, capitalized):
    words = []
    words.append( choice(capitalized) )
    words.extend( [choice(normal) for word in range(randint(3, 15))] )
    return ' '.join(words) + '.'

def generate_paragraph(normal, capitalized):
    sentences = [generate_sentence(normal, capitalized) for _ in range(randint(5, 10))]
    return ' '.join(sentences)

def main():
    normal, capitalized = get_dictionary()

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
        paragraph = generate_paragraph(normal, capitalized)
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
