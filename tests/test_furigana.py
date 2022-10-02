import pytest

from furigana.furigana import split_furigana, split_okurigana, Text


@pytest.mark.parametrize(["text", "expected_split"], [
    ("1ヶ月", [
        Text(text='1', furigana=None),
        Text(text='ヶ', furigana=None),
        Text(text='月', furigana='げつ'),
    ]),
    ("雁ヶ音", [
        Text(text='雁', furigana='かり'),
        Text(text='ヶ', furigana=None),
        Text(text='音', furigana='おん'),
    ]),
    ("Spaces won't be forgotten", [
        Text(text='Spaces', furigana=None),
        Text(text=' ', furigana=None),
        Text(text='won', furigana=None),
        Text(text="'", furigana=None),
        Text(text='t', furigana=None),
        Text(text=' ', furigana=None),
        Text(text='be', furigana=None),
        Text(text=' ', furigana=None),
        Text(text='forgotten', furigana=None),
    ]),
    ("２０００年", [
        Text(text='２０００年', furigana='にせんねん')
    ]),
    ("1986年", [
        Text(text='1986年', furigana='せんきゅうひゃくはちじゅうろくねん')
    ]),
    ("元ハーバード大学", [
        Text(text='元', furigana='もと'),
        Text(text='ハーバード', furigana=None),
        Text(text='大学', furigana='だいがく'),
    ]),
    ("１週間して、そのニュースは本当になった", [
        Text(text='１週間', furigana='いっしゅうかん'),
        Text(text='し', furigana=None),
        Text(text='て', furigana=None),
        Text(text='、', furigana=None),
        Text(text='その', furigana=None),
        Text(text='ニュース', furigana=None),
        Text(text='は', furigana=None),
        Text(text='本当', furigana='ほんとう'),
        Text(text='に', furigana=None),
        Text(text='なっ', furigana=None),
        Text(text='た', furigana=None),
    ]),
])
def test_split_furigana(text, expected_split):
    assert split_furigana(text) == expected_split


@pytest.mark.parametrize(["text", "hiragana", "expected_split"], [
    (
        # Reverse parsing example #1
        "人となり", "ひととなり", [
            Text(text='人', furigana='ひと'),
            Text(text='となり', furigana=None)
        ]
    ),
    (
        # Reverse parsing example #2
        "短かっ", "みじかかっ", [
            Text(text='短', furigana='みじか'),
            Text(text='かっ', furigana=None)
        ]
    ),
    (
        # ヶ used for が in location name
        "青木ヶ原", "あおきがはら", [
            Text(text='青木', furigana='あおき'),
            Text(text='ヶ', furigana=None),
            Text(text='原', furigana='はら'),
        ]
    ),
    (
        # Fallback in case of kana mismatch between text and hiragana
        "あ。あ", "あのあ", [Text(text='あ。あ', furigana='あのあ')]
    ),
    (
        # Dealing with non kanji non kana characters such as "・"
        "トム・ソーヤーの冒険", "とむそーやーのぼうけん", [
            Text(text='トム・ソーヤーの', furigana=None),
            Text(text='冒険', furigana='ぼうけん')
        ]
    ),
    (
        # Dealing with non kanji non kana characters such as "・"
        "銃・病原菌・鉄", "じゅうびょうげんきんてつ", [
            Text(text='銃・病原菌・鉄', furigana='じゅうびょうげんきんてつ')
        ]
    ),
    ("出会う", "であう", [
        Text(text='出会', furigana='であ'),
        Text(text='う', furigana=None),
    ]),
    ("明るい", "あかるい", [
        Text(text='明', furigana='あか'),
        Text(text='るい', furigana=None),
    ]),
    ("駆け抜け", "かけねけ", [
        Text(text='駆', furigana='か'),
        Text(text='け', furigana=None),
        Text(text='抜', furigana='ね'),
        Text(text='け', furigana=None),
    ]),
    ("お話し", "おはなし", [
        Text(text='お', furigana=None),
        Text(text='話', furigana="はな"),
        Text(text='し', furigana=None),
    ]),
    ("本当に", "ほんとーに", [
        Text(text='本当', furigana='ほんとー'),
        Text(text='に', furigana=None),
    ]),
    ("２０", "にじゅう", [
        Text(text='２０', furigana="にじゅう"),
    ]),
    (
        # Some entries may have an incorrect reading
        # that does not match in terms of length.
        # In this case we just ignore the reading
        "爆売れ", "うれ", [
            Text(text='爆売れ', furigana=None),
        ]
    ),
])
def test_split_okurigana(text, hiragana, expected_split):
    assert split_okurigana(text, hiragana) == expected_split
