furigana
========

Generate furigana(振り仮名) from Japanese

It uses `MeCab <http://taku910.github.io/mecab/>`__ (a Natural Language
Toolkit) to split Japanese into words, and superscript it with furigana
(振り仮名).

Example:
--------

input
~~~~~

::

    print_plaintext('澱んだ街角で僕らは出会った')

output
~~~~~~

澱(よど)んだ街角(まちかど)で僕(ぼく)らは出(で)会(あ)った

input
~~~~~

::

    print_html('お茶にお煎餅、よく合いますね')

output
~~~~~~

お茶(ちゃ)にお煎餅(せんべい)、よく合(あ)いますね

Usage
-----

::

    $ python3 furigana.py '活版印刷の流れを汲む出版作業では'

Dependency
==========

See https://pypi.python.org/pypi/mecab-python3/0.7 run below commands on
ubuntu

::

    sudo apt-get install libmecab-dev
    sudo apt-get install mecab mecab-ipadic-utf8
    pip install mecab-python3
