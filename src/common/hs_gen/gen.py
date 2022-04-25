"""
This file contains a class to generate random paragraphs
using Hunspell dicts.

Confused? Think Lorem Ipsum without Latin. Or with some surprise Latin.

Installation of the dicts is different for different distros:
* Alpine: apk add hunspell-en
* Arch / Artix: doas pacman -S hunspell-en_gb
* Debian: apt-get install hunspell-en-gb -y
"""

from string import ascii_letters
from random import choice, randint

class ParagraphGenerator:
    """A random paragraph generator class that uses the
       Hunspell dictionary."""

    def __init__(
        self,
        dict_path='/usr/share/hunspell/en_GB-large.dic',
        min_sentence_length=4,
        max_sentence_length=16,
        min_sentences=5,
        max_sentences=10
    ):
        self.dict_path = dict_path
        self.normal, self.capitalized = self.get_dictionary()
        self.min_sentence_length = min_sentence_length
        self.max_sentence_length = max_sentence_length
        self.min_sentences = min_sentences
        self.max_sentences = max_sentences

    def get_dictionary(self):
        dict_words = []
        with open(self.dict_path, 'r') as dict_file:
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

    def generate_sentence(self):
        """
        Returns:

            str: a single sentence
        """
        words = [
            choice(self.capitalized),
            *[
                choice(self.normal)
                for _ in range(randint(
                    self.min_sentence_length - 1,
                    self.max_sentence_length - 1
                ))
            ]
        ]
        sign = choice(['.', '?', '!'])
        return ' '.join(words) + sign

    def generate_paragraph(self):
        """
        Returns:

            str: a single paragraph
        """
        sentences = [
            self.generate_sentence()
            for _ in range(randint(self.min_sentences, self.max_sentences))
        ]
        return ' '.join(sentences)
