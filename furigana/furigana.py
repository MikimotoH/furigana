#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import MeCab
import re
import jaconv
import unicodedata
from collections import namedtuple

Text = namedtuple('Text', ['text', 'furigana'])

def is_kanji(ch):
    #also include 々 as Kanji
    return 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(ch)

def is_hiragana(ch):
    return 'HIRAGANA' in unicodedata.name(ch)

def is_katakana(ch):
    return 'KATAKANA' in unicodedata.name(ch)

def is_normal_character(ch):
    return is_hiragana(ch) or is_katakana(ch)

def split_okurigana(text, hiragana):

    split = []
    i = 0
    j = 0

    while i < len(text):
        start_i = i
        start_j = j
        # take care of hiragana only parts
        if(is_normal_character(text[i])):
            while i < len(text) and j < len(hiragana) and is_normal_character(text[i]):
                i += 1
                j += 1
        
            split.append(Text(text[start_i:i], None))

            if(i >= len(text)):
                break

            start_i = i
            start_j = j

        # find next non kanji
        while i < len(text) and not is_normal_character(text[i]):
            i += 1

        #if there only kanji left
        if(i >= len(text)):
            split.append(Text(text[start_i:i], hiragana[start_j:len(hiragana)]))
            break
        
        #get reading of kanji
        # j-start_j < i - start_i every kanji has at least one sound associated with it
        while j < len(hiragana) and ((hiragana[j] != text[i] and jaconv.hira2kata(hiragana[j]) != text[i]) or j-start_j < i - start_i):
            j += 1

        split.append(Text(text[start_i:i], hiragana[start_j:j]))
        
    return split


def split_furigana(text):
    """ MeCab has a problem if used inside a generator ( use yield instead of return  )
    The error message is:
    ```
    SystemError: <built-in function delete_Tagger> returned a result with an error set
    ```
    It seems like MeCab has bug in releasing resource
    """
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('') # 空でパースする必要がある
    node = mecab.parseToNode(text)
    ret = []

    while node is not None:
        texts = parse_node(node)
        if texts:
            ret.extend(texts)

        node = node.next

    return ret

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
            string += "<ruby>%s<rt>%s</rt></ruby>" %(pair.text, pair.furigana)
        else:
            string+= pair.text
    return(string)


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
