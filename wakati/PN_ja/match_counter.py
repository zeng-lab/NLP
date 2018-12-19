import MeCab
import re
import urllib.request
import chardet
import codecs   #unicodeError対策
import time
import argparse
from bs4 import BeautifulSoup

class Mecab:
    def __init__(self):
        self.s = 0
        self.e = 200000
        self.stops = 2000000
        self.tagger = MeCab.Tagger('-Owakati -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
        self.All = 0

    def re_def(self,filepass):
        with codecs.open(filepass, 'r', encoding='utf-8', errors='ignore')as f:
        #with open(filepass, 'r')as f:
            l = ""
            re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
            re_full = re.compile(r'[︰-＠]')  # 全角記号
            re_full2 = re.compile(r'[、・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〇〔〕…――――─◇]')  # 全角で取り除けなかったやつ 
            re_comma = re.compile(r'[。]')  # 全角で取り除けなかったやつ
            re_url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+')
            re_tag = re.compile(r"<[^>]*?>")    #HTMLタグ
            re_n = re.compile(r'\n')  # 改行文字
            re_space = re.compile(r'[\s+]')  #１以上の空白文字
            pattern = "(.*)　(.*)"  #全角スペースで分ける
            start_time = time.time()
            for line in f:
                if '○' in line: #○からスペースまで名前なので取り除く
                    sep = re.search(pattern,line)
                    line = line.replace(sep.group(1),"")
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

    def Match(self):
        meishi = ""
        pattern = "(.):(.*)"
        ja_dic = ""
        #with open("list.dic","r",encoding="utf-8") as f:
        #    for i in f:
        #        sep = re.search(pattern,i)
        #        i = i.replace(sep.group(2),"")
        #        i = i.replace(":","")
        #        #print(i)
        #        meishi += i
        #meishi = re.split('[\n]', meishi)
        url = 'http://www.lr.pi.titech.ac.jp/~takamura/pubs/pn_ja.dic'
        with urllib.request.urlopen(url) as res:
            html = res.readline().decode("Shift_JIS")
            while html:
                sep = re.search(pattern,html)   
                #print(sep.group(2))
                html = html.replace(sep.group(2),"")
                ja_dic += html.replace(":","")
                html = res.readline().decode("Shift_JIS")
        ja_dic = re.split('[\n]', ja_dic)
        #print(ja_dic)
        return ja_dic

    def owakati(self,all_words):
        wakatifile = []
        while True:
            w = all_words[self.s:self.e]
            wakatifile.extend(self.tagger.parse(w).split("\n"))
            if self.e > self.stops or self.e > len(all_words) : 
                break
            else:
                self.s = self.e
                self.e += 200000
        return wakatifile

    def counting(self,all_words):
        print("総文字数:{0}\t({1}万字)".format(len(all_words), len(all_words)/10000))
        tmp_list = []
        match = self.Match()  #Matchぱたーん
        setcount = 0
        notMatch = 0
        wakati = self.owakati(all_words)  #分かち書きアンド形態素解析
        for addlist in wakati:
            #tmp_list.extend(re.split('[\t,]', addlist))  # 空白と","で分割
            tmp_list = re.split('[ ,]', addlist)  # 空白と","で分割
            #tmp_list = set(tmp_list)
            for addword in tmp_list:
                if addword in match:               
                    setcount += 1
                #print(setcount)
                else:
                    notMatch += 1

        return setcount ,notMatch

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--out', '-o' , type=str)
    args = parser.parse_args()
    
    mecab = Mecab()
    words = mecab.re_def(args.input)
    stime = time.time()
    hitword , nohit= mecab.counting(words)
    etime = time.time() - stime
    print("処理時間:",etime)
    print("ヒットした単語数（重複もカウント）：" , hitword)
    print("ヒットしなかった数：" , nohit)
