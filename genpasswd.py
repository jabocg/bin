#!/usr/bin/env python3
"""Generate a random(enough) password based on the pattern '##@Wordword'."""

import argparse
import re
import secrets


SYMBOLS = [')', '!', '@', '#', '$', '%', '^', '&', '*', '(']
LEFT_LETTERS = 'qwertasdfgzxcvb'
RIGHT_LETTERS = 'poiuylkjhmn'
WORDS_FILE = '/usr/share/dict/words'


def main():
    """Generate the password."""
    args = parse_args()
    passwd = []

    wordlen = (args.length - 3) // 2
    if (args.length - 3) & 1:
        # length is odd, have to have extra character somewhere
        if wordlen & 1:
            # wordlen is odd, make first word even length
            wordlen1 = wordlen + 1
            wordlen2 = wordlen
        else:
            # wordlen is even, make second word odd length
            wordlen1 = wordlen
            wordlen2 = wordlen + 1
    else:
        wordlen1 = wordlen
        wordlen2 = wordlen

    nums = get_numbers()
    passwd.append(str(nums[0]))
    passwd.append(str(nums[1]))
    passwd.append(SYMBOLS[nums[2]])

    if nums[2] > 6 or nums[2] == 0:
        side = 'r'
    elif nums[2] > 0:
        side = 'l'

    passwd.append(find_word(wordlen1, side))
    passwd.append(find_word(wordlen2, side, capitol=False))

    print(''.join(passwd))


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--length', type=int,
                        help='min length of password',
                        default=16)
    return parser.parse_args()


def find_word(length, side, capitol=True):
    """Find a word in the dictionary that matches a pattern."""
    with open(WORDS_FILE, mode='r') as wf:
        all_words = wf.read()
    if length & 1:
        # odd word length, add end character
        pstr = '^(?:[{}][{}]){{{}}}[{}]$'
    else:
        # even word length, no additional characters
        pstr = '^(?:[{}][{}]){{{}}}$'
    if side == 'l':
        pattern = re.compile(pstr.format(LEFT_LETTERS,
                                         RIGHT_LETTERS,
                                         length // 2,
                                         LEFT_LETTERS),
                             re.MULTILINE)
    else:
        pattern = re.compile(pstr.format(RIGHT_LETTERS,
                                         LEFT_LETTERS,
                                         length // 2,
                                         RIGHT_LETTERS),
                             re.MULTILINE)
    words = re.findall(pattern, all_words)

    word = secrets.choice(words)

    if capitol:
        return '{}{}'.format(word[0].upper(), word[1:])
    else:
        return word


def get_numbers():
    """Return randomly chosen numbers."""
    return (secrets.randbelow(10),
            secrets.randbelow(10),
            secrets.randbelow(10))


if __name__ == "__main__":
    main()
