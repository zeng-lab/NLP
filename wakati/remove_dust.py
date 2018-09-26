import MeCab
import re

doc = "日 本語1の自2然言  語処理は23し   ん9どい かもしれな00い け もの はい0 てもの け も の132 はい  ない"
tagger = MeCab.Tagger("-Owakati")

#compileしたほうが処理が速いって
pat = r'[0-9\s+]'
pat = re.compile(pat)
doc = pat.sub("", doc)  #数字を取り除きまふ
print(doc)
res = tagger.parse(doc).split()
print(res)
if res[-1] == "\n":
   res = res[:-1]

a = ["日本語", "自然言語処理"]

for word in a:
    try:
        res2 = res.remove(word)
    except ValueError:
        pass

print(res)