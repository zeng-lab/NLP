import MeCab
import re
import urllib3
import codecs   #unicodeError対策
import time
import argparse
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

class Mecab:
    def __init__(self):
        self.s = 0
        self.e = 200000
        self.stops = 2000000
        self.tagger = MeCab.Tagger()
        self.All = 0

    def re_def(self,filepass):
        with codecs.open(filepass, 'r', encoding='utf-8', errors='ignore')as f:
        #with open(filepass, 'r')as f:
            l = ""
            re_half = re.compile(r'[!-~]')  # 半角記号,数字,英字
            re_full = re.compile(r'[︰-＠]')  # 全角記号
            re_full2 = re.compile(r'[、・’〜：＜＞＿｜「」｛｝【】『』〈〉“”○〔〕…――――◇]')  # 全角で取り除けなかったやつ
            #re_full2 = re.compile(r'[、〜＿―――─―◇○]')  # くくり文字以外
            re_comma = re.compile(r'[。]')  # 読点のみ
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

    def owakati(self, all_words):
        wakatifile = []
        while True:
            w = all_words[self.s:self.e]
            wakatifile.extend(self.tagger.parse(w).split("\n"))
            if self.e > self.stops or self.e > len(all_words):
                break
            else:
                self.s = self.e
                self.e += 200000
        return wakatifile

    def counting(self,all_words):
        dicts = {}  # 単語をカウントする辞書
        print("総文字数:{0}\t({1}万字)".format(len(all_words),len(all_words)/10000))
        ALL = 0 #単語のカウント
        mem = 0 #一定単語以上か判別
        #re_hiragana = re.compile(r'[あ-んア-ン一-鿐].')    #ひらがな2文字以上にヒットする正規表現
        sloths = self.sloth_words() #slothのlist
        if len(all_words) > 2000000:
            mem = 1
        while True:
            word_list = []
            wakati = self.owakati(all_words) #分かち書きアンド形態素解析
            for addlist in wakati:
                addlist = re.split('[\t,]', addlist)  # 空白と","で分割
                """
                for stopword in sloths:  #ストップワードを取り除く
                    if stopword == addlist[0]:
                        addlist = []
                        break
                    #while stopword in addlist[0]:
                    #    del addlist[0]
                """
                if addlist == [] or addlist[0] == 'EOS' or addlist[0] == '' or addlist[0] == 'ー' or addlist[0] == '*':
                    pass
                elif addlist[1] == '名詞':  #名詞のみカウント
                    ALL += 1
                    #elif addlist[1] == '名詞' and addlist[2] == '一般' or addlist[1] == '動詞' and addlist[2] == '自立' or addlist[1] == '形容詞' and addlist[2] == '自立' or addlist[1] == '副詞' and addlist[2] == '一般':
                    if addlist[1] == '名詞' and addlist[2] == '一般' or addlist[1] == '名詞' and addlist[2] == '固有名詞' :#and not addlist[3] == '人名':
                        #print(addlist)  #6番目に未然形とか連用タ接続
                        #del addlist[:7] #発言の単語ではなくその意味だけに丸める
                        for stopword in sloths:  # ストップワードを取り除く カウントするとこだけ処理にして処理時間削減
                            if stopword == addlist[0]:
                                addlist = []
                                break
                        if addlist:
                            word_list.append(addlist)  #listごとに区切るのでappendでextendだとつながる
                else:
                    pass
            for count in word_list:
                if count[0] not in dicts:
                    dicts.setdefault(count[0], 1)
                else:
                    dicts[count[0]] += 1
            ###メモリ解放###
            if mem:
                #for n, c in dicts.items():
                #    if c < len(all_words)/10**5:
                #        del n, c
                if len(all_words) < self.stops:
                    del wakati, addlist, word_list
                    break
                else:
                    del addlist
                    print("{}万字まで終わったよ".format(self.stops/10000))
                    self.stops += 2000000
                    self.s = self.e
                    self.e += 200000
            else:
                break
        self.All = ALL  #総単語数
        return dicts

    def plot(self,countedwords):
        counts = {}
        c = 1
        show = 20 #何件表示する？
        for k, v in sorted(countedwords.items(), key=lambda x: x[1], reverse=True):  # 辞書を降順に入れる
            counts.update( {str(k):int(v)} )
            c += 1
            if c > show:
            ###結果の出力###
            #    with open("result_wakati.txt", "w") as f:
            #        f.write(str(counts))
               break
        plt.figure(figsize=(15, 5)) #これでラベルがかぶらないくらい大きく
        plt.title('頻繁に発言したワードベスト{0} 総単語数{1} 単語の種類数{2}'.format(show,self.All,len(countedwords)), size=16)
        plt.bar(range(len(counts)), list(counts.values()), align='center')
        plt.xticks(range(len(counts)), list(counts.keys()))
        # 棒グラフ内に数値を書く
        for x, y in zip(range(len(counts)), counts.values()):
            plt.text(x, y, y, ha='center', va='bottom') #出現回数
            plt.text(x, y/2, "{0}%".format(round((y/self.All*100),3)),ha='center',va='bottom')  #パーセンテージ
        plt.tick_params(width=2, length=10) #ラベル大きさ 
        plt.tight_layout()  #整える
        plt.show()

    def Search(self, countedwords,search):
        results = {}
        for k, v in countedwords.items():
            if search == k:
                results.update({str(k): int(v)})

        return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--save', '-s' , type=str)
    parser.add_argument('--look', '-l' , type=str)
    args = parser.parse_args()


    mecab = Mecab()
    words = mecab.re_def(args.input)
    stime = time.time()
    c = mecab.counting(words)
    etime = time.time() - stime
    print("解析処理時間",etime)
    if args.save:
        with open(args.save, "w") as f:
            for key,value in c.items():
                f.write(f'{key} {value}\n')
    s = input("検索ワードorPlot(1)：")
    if s == "1":
        mecab.plot(c)
    else:
        while True:
            print(mecab.Search(c,s))
            s = input("検索ワード or end(push 0)：")
            if s == "0":
                break