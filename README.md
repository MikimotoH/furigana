# furigana
Generate furigana from Japanese

It uses [MeCab](http://taku910.github.io/mecab/) (a Natural Language Toolkit) to split Japanese into words, and superscript it with furigana (振り仮名).

## Example:
### input
```
print_html('澱んだ街角で僕らは出会った')
```
### output
<ruby><rb>澱</rb><rt>よど</rt></ruby>
ん
だ
<ruby><rb>街角</rb><rt>まちかど</rt></ruby>
で
<ruby><rb>僕</rb><rt>ぼく</rt></ruby>
ら
は
<ruby><rb>出</rb><rt>で</rt></ruby>
<ruby><rb>会</rb><rt>あ</rt></ruby>
っ
た

### input
print_html('お茶にお煎餅、よく合いますね')
### output
お
<ruby><rb>茶</rb><rt>ちゃ</rt></ruby>
に
お
<ruby><rb>煎餅</rb><rt>せんべい</rt></ruby>
、
よく
<ruby><rb>合</rb><rt>あ</rt></ruby>
い
ます
ね

