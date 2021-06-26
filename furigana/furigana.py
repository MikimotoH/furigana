#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
import unicodedata
from collections import namedtuple
from xml.sax.saxutils import escape

import MeCab
import jaconv

mecab = MeCab.Tagger("-Ochasen")

Text = namedtuple('Text', ['text', 'furigana'])

def is_kanji(ch):
    #also include 々 as Kanji
    return 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(ch)

def is_hiragana(ch):
    return 'HIRAGANA' in unicodedata.name(ch) and ch != "・"

def is_katakana(ch):
    return 'KATAKANA' in unicodedata.name(ch) and ch != "・"

def is_kana_character(ch):
    return is_hiragana(ch) or is_katakana(ch)

def is_kanji_or_number(ch):
    return is_kanji(ch) or ch in "0123456789０１２３４５６７８９"

def split_okurigana(text, hiragana):
    logging.debug(f'Split okurigana for "{text}" / "{hiragana}"')

    split = []
    i = 0  # cursor on the text
    j = 0  # cursor on the hiragana

    while i < len(text):
        start_i = i
        start_j = j

        logging.debug(f'Taking care non kanji parts. i={i}, j={j} ("{text[i]}" / "{hiragana[j]}")')
        if not is_kanji_or_number(text[i]):
            while i < len(text) and j < len(hiragana) and not is_kanji_or_number(text[i]):
                # Increment the hiragana cursor, except for punctuation (not kana nor kanji),
                # which is absent from the hiragana str !
                if is_kana_character(text[i]):
                    if hiragana[j] != text[i] and jaconv.hira2kata(hiragana[j]) != text[i]:
                        # FIXME Handle this case properly ! Example: 人[ひと]となり
                        logging.error(f"Kana {hiragana[j]} did not match character {text[i]} !")
                        # Fallback by returning all the remaining text with all the hiragana as furigana
                        split.append(Text(text[start_i:], hiragana[start_j:]))
                        return split
                    j += 1

                i += 1

            logging.debug(f'Reached end of non kanji part. i={i}, j={j} ("{text[start_i:i]}" / "{hiragana[start_j:j]}")')
            split.append(Text(text[start_i:i], None))

            if i >= len(text):
                break

            start_i = i
            start_j = j

        # find next kana
        logging.debug(f'Find next kana in text "{text[i:]}". i={i}')
        while i < len(text) and not is_kana_character(text[i]):
            i += 1

        if i >= len(text):
            logging.debug(f'Only kanji left. i={i}, j={j} ("{text[start_i:i]}" / "{hiragana[start_j:len(hiragana)]}")')
            split.append(Text(text[start_i:i], hiragana[start_j:len(hiragana)]))
            break
        
        logging.debug(f'Get reading for "{text[start_i:i]}". j={j}')
        while (
            j < len(hiragana)
            and (
                (hiragana[j] != text[i] and jaconv.hira2kata(hiragana[j]) != text[i])
                or j - start_j < i - start_i  # every kanji has at least one sound associated with it
             )
        ):
            j += 1

        logging.debug(f'Got reading "{hiragana[start_j:j]}" for "{text[start_i:i]}"')

        split.append(Text(text[start_i:i], hiragana[start_j:j]))
        
    return split


def split_furigana(text, preserve_spaces=True):
    """ MeCab has a problem if used inside a generator ( use yield instead of return  )
    The error message is:
    ```
    SystemError: <built-in function delete_Tagger> returned a result with an error set
    ```
    It seems like MeCab has bug in releasing resource
    """
    mecab.parse('') # 空でパースする必要がある
    node = mecab.parseToNode(text)
    ret = []

    cursor = 0
    while node is not None:
        if preserve_spaces:
            new_cursor, spaces = detect_spaces(cursor, node, text)
            cursor = new_cursor
            if spaces:
                ret.append(Text(spaces, None))

        texts = parse_node(node)
        if texts:
            ret.extend(texts)

        node = node.next

    return ret


def detect_spaces(cursor, node, text):
    spaces = None
    origin = node.surface
    if origin:
        origin_start = text.index(origin, cursor)
        origin_end = origin_start + len(origin)
        if cursor < origin_start:
            spaces = text[cursor:origin_start]
        cursor = origin_end
    return cursor, spaces


def parse_node(node):
    # originが空のとき、漢字以外の時はふりがなを振る必要がないのでそのまま出力する
    # sometimes MeCab can't give kanji reading, and make node-feature have less than 7 when splitted.
    origin = node.surface
    if origin != "" and len(node.feature.split(",")) > 7 and any(is_kanji(_) for _ in origin):
        kana = node.feature.split(",")[7]  # 読み仮名を代入
        hiragana = jaconv.kata2hira(kana)
        return split_okurigana(origin, hiragana)
    elif origin:
        return [Text(origin, None)]
    else:
        return []


def create_furigana_html(text):
    string = ""
    for pair in split_furigana(text):
        if pair.furigana:
            string += "<ruby>%s<rt>%s</rt></ruby>" % (xmlescape(pair.text), xmlescape(pair.furigana))
        else:
            string += xmlescape(pair.text)
    return(string)


def xmlescape(data):
    return escape(data, entities={
        "'": "&apos;",
        "\"": "&quot;"
    })


def return_html(text):
    return create_furigana_html(text)


def print_html(text):
    print(create_furigana_html(text))


def print_plaintext(text):
    string = ""
    for pair in split_furigana(text):
        if pair.furigana:
            string += "%s(%s)"%(pair.text, pair.furigana)
        else:
            string+= pair.text
    print(string)


def main():
    text = sys.argv[1]
    print_html(text)


if __name__ == '__main__':
    main()
