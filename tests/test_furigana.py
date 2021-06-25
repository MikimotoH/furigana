import pytest

from furigana.furigana import split_furigana, split_okurigana, Text


@pytest.mark.parametrize(["text", "expected_split"], [
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
    ("銃・病原菌・鉄", "じゅうびょうげんきんてつ", [
        Text(text='銃・病原菌・鉄', furigana='じゅうびょうげんきんてつ')
    ]),
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
])
def test_split_okurigana(text, hiragana, expected_split):
    assert split_okurigana(text, hiragana) == expected_split