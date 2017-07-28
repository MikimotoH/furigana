#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# $ python -m hello

import sys
from furigana.furigana import split_furigana

def print_html(text):
    for pair in split_furigana(text):
        if len(pair)==2:
            kanji,hira = pair
            print("<ruby><rb>{0}</rb><rt>{1}</rt></ruby>".
                    format(kanji, hira), end='')
        else:
            print(pair[0], end='')
    print('')


def print_plaintext(text):
    for pair in split_furigana(text):
        if len(pair)==2:
            kanji,hira = pair
            print("%s(%s)" % (kanja,hira), end='')
        else:
            print(pair[0], end='')
    print('')


def main():
    text = sys.argv[1]
    print_plaintext(text)


if __name__ == '__main__':
    main()
