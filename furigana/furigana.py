#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import MeCab
import re
import jaconv
import unicodedata


def is_kanji(ch):
    return 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(ch)


def is_hiragana(ch):
    return 'HIRAGANA' in unicodedata.name(ch)


def split_okurigana_reverse(text, hiragana):
    """ 
      tested:
        お茶(おちゃ)
        ご無沙汰(ごぶさた)
        お子(こ)さん
    """
    yield (text[0],)
    yield from split_okurigana(text[1:], hiragana[1:])


def split_okurigana(text, hiragana):
    """ 送り仮名 processing
      tested: 
         * 出会(であ)う
         * 明(あか)るい
         * 駆(か)け抜(ぬ)け
    """
    if is_hiragana(text[0]):
        yield from split_okurigana_reverse(text, hiragana)
    if all(is_kanji(_) for _ in text):
        yield text, hiragana
        return
    text = list(text)
    ret = (text[0], [hiragana[0]])
    for hira in hiragana[1:]:
        for char in text:
            if hira == char:
                text.pop(0)
                if ret[0]:
                    if is_kanji(ret[0]):
                        yield ret[0], ''.join(ret[1][:-1])
                        yield (ret[1][-1],)
                    else:
                        yield (ret[0],)
                else:
                    yield (hira,)
                ret = ('', [])
                if text and text[0] == hira:
                    text.pop(0)
                break
            else:
                if is_kanji(char):
                    if ret[1] and hira == ret[1][-1]:
                        text.pop(0)
                        yield ret[0], ''.join(ret[1][:-1])
                        yield char, hira
                        ret = ('', [])
                        text.pop(0)
                    else:
                        ret = (char, ret[1]+[hira])
                else:
                    # char is also hiragana
                    if hira != char:
                        break
                    else:
                        break


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
        origin = node.surface # もとの単語を代入
        if not origin:
            node = node.next
            continue

        # originが空のとき、漢字以外の時はふりがなを振る必要がないのでそのまま出力する
        if origin != "" and any(is_kanji(_) for _ in origin):
            kana = node.feature.split(",")[7] # 読み仮名を代入
            hiragana = jaconv.kata2hira(kana)
            for pair in split_okurigana(origin, hiragana):
                ret += [pair]
        else:
            if origin:
                ret += [(origin,)]
        node = node.next
    return ret


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
    print_html(text)


if __name__ == '__main__':
    main()

