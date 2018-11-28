import MeCab
import re
import urllib3
import codecs   #unicodeError対策
import time
from bs4 import BeautifulSoup

class Mecab:
    def __init__(self):
        self.s = 0
        self.e = 200000
        self.stops = 2000000
        self.tagger = MeCab.Tagger('-Owakati')
        self.All = 0

    def re_def(self,filepass):
        with codecs.open(filepass, 'r', encoding='utf-8', errors='ignore')as f:
        #with open(filepass, 'r')as f:
            l = ""
            re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
            re_full = re.compile(r'[︰-＠]')  # 全角記号
            re_full2 = re.compile(r'[、・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〇〔〕…――――─◇]')  # 全角で取り除けなかったやつ
            #re_full2 = re.compile(r'[、〜＿―――─―◇○]')  # くくり文字以外
            re_comma = re.compile(r'[。]')  # 全角で取り除けなかったやつ
            re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+')
            re_tag = re.compile(r"<[^>]*?>")    #HTMLタグ
            re_n = re.compile(r'\n')  # 改行文字
            re_space = re.compile(r'[\s+]')  #１以上の空白文字
            start_time = time.time()
            for line in f:
                line = re_half.sub("", line)
                line = re_full.sub("", line)
                line = re_url.sub("", line)
                line = re_tag.sub("",line)
                line = re_n.sub("", line)
                line = re_space.sub("", line)
                line = re_full2.sub(" ", line)
                line = re_comma.sub("\n",line)  #読点で改行しておく
                l += line
        #with open("tmp.csv",'w') as F:
        #    F.write(l)
        end_time = time.time() - start_time
        print("無駄処理時間",end_time)
        return l

    def sloth_words(self):    #slothwordのlist化
        ###sloth_words###
        sloth = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
        http = urllib3.PoolManager() #urlib3系のおまじない
        slothl_file = http.request('GET', sloth)
        soup = BeautifulSoup(slothl_file.data, 'lxml')
        soup = str(soup).split()  # soupは文字列じゃないので注意
        soup.pop(0) #htmlタグを殲滅せよ
        soup.pop()                      
        #SlothLibに存在しないストップワードを自分で追加↓
        mydict = ['君','先','いわば']
        soup.extend(mydict)

        ###sloth_singleword###
        sloth_1 = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/OneLetterJp.txt'
        slothl_file2 = http.request('GET', sloth_1)
        soup2 = BeautifulSoup(slothl_file2.data, 'lxml')
        soup2 = str(soup2).split()  # soupは文字列じゃないので注意
        soup2.pop(0)  # htmlタグを殲滅せよ
        soup2.pop()

        soup.extend(soup2)  #1つにまとめる
        return soup

    def owakati(self,all_words):
        wakatifile = []
        while len(all_words):
            w = all_words[self.s:self.e]
            wakatifile += (self.tagger.parse(w).split("\n"))
            #wakatifile.extend(tagger.parse(w).split("\n"))
            if self.e > len(all_words) or self.e > self.stops:
                break
            else:
                self.s = self.e
                self.e += 200000
        return wakatifile

    def counting(self,all_words):
        print("総文字数:", len(all_words))
        wakati_list = ""
        #ALL = 0 #単語のカウント
        mem = 0 #一定単語以上か判別
        sloths = self.sloth_words()  #slothのlist
        if len(all_words) > 2000000:    #単語数オーバーなら再帰
            mem = 1
        while True:
            wakati = self.owakati(all_words) #分かち書きアンド形態素解析
            for addlist in wakati:
                addlist = addlist.split()  #単語ごとにlistに分ける
                break
            for addword in addlist:
                if addword in sloths:
                    pass
                else:
                    wakati_list += addword + ' '    #空白で区切る
            ###語数オーバーの時###
            if mem:
                if len(all_words) < self.stops:
                    break
                else:
                    print("文字数オーバーなので200万文字ごとに再帰ちう")
                    self.stops += 2000000
                    self.s = self.e
                    self.e += 200000
            else:
                break
        return wakati_list

if __name__ == '__main__':
    mecab = Mecab()
    words = mecab.re_def("statements/edano_diet.csv")
    stime = time.time()
    c = mecab.counting(words)
    etime = time.time() - stime
    print(etime)
    with open("statements/edano_diet_wakati.csv", "w") as f:
        f.write(c)