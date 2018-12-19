import urllib
import untangle
import urllib.parse
from bs4 import BeautifulSoup
import os
import sys

def scrape(path):
    start = '1'
    i = 0
    Reco = ""
    if os.path.exists(path):
        a = int(input("ファイルあるけど上書きする？:yes(0) or no(1)："))
        if a:
            print("しゅーりょー")
            sys.exit()
        else:
            with open(path,'w') as f:
                f.write("")

    while True:
        #keyword = '安倍晋三'
        startdate = '2016-01-01'
        #enddate = '2018-12-31'
        maxreco = '100' #最大１００件
        #meeting = '本会議 予算委員会'
        #urllib.parse.quoteが日本語をコーディングしてくれる
        url = 'http://kokkai.ndl.go.jp/api/1.0/speech?'+urllib.parse.quote('startRecord=' + start
                                                                           + '&maximumRecords=' + maxreco
                                                                           #+ '&speaker=' + keyword
                                                                           #+ '&nameOfMeeting=' + meeting
                                                                           + '&from=' + startdate)
                                                                           #+ '&until=' + enddate)
        obj = untangle.parse(url)
        #print(obj.data.numberOfRecords.cdata, type(obj.data.records.record))
        art = obj.data.numberOfRecords.cdata
        for record in obj.data.records.record:
            speechrecord = record.recordData.speechRecord
            #print(speechrecord.date.cdata,speechrecord.speech.cdata)
            Reco += speechrecord.speech.cdata
        Reco += '\n'
        if not i%300:   #300件超えるならここでカキコ
            with open(path, 'a+') as f:
                f.write(Reco)
            Reco = ""
        try:    #最後にエラーで終わるからここでにゃーん
            start = obj.data.nextRecordPosition.cdata
        except AttributeError:
            print("にゃーんえらー")
            break
        i += 100
        if i > int(art):
            print("件数到達")
            break
        print("{0}件中{1}件目".format(art,i))
    return Reco
        
if __name__ == '__main__':
    path = "diet2016to_now.csv"
    r = scrape(path)
    # w =カキコ,r =読み,a =追加カキコ,w+ =全部消してカキコ,r+ =既に書かれている内容を上書き,a+ =既に書かれている内容に追記
    with open(path, 'a+') as f: #残りをかきこ
        f.write(r)