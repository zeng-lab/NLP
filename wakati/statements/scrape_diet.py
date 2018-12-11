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
        a = int(input("ファイルあるけど上書きする？:yes(0) or no(1)"))
        if a:
            print("しゅーりょー")
            sys.exit()

    while start != None:
        keyword = '安倍晋三'
        startdate = '2018-01-01'
        enddate = '2018-12-31'
        #meeting = '本会議 予算委員会'
        #urllib.parse.quoteが日本語をコーディングしてくれる
        url = 'http://kokkai.ndl.go.jp/api/1.0/speech?'+urllib.parse.quote('startRecord=' + start
                                                                           + '&maximumRecords=100&speaker=' + keyword
                                                                           #+ '&nameOfMeeting=' + meeting
                                                                           + '&from=' + startdate
                                                                           + '&until=' + enddate)
        obj = untangle.parse(url)
        #print(obj.data.numberOfRecords.cdata, type(obj.data.records.record))
        for record in obj.data.records.record:
            speechrecord = record.recordData.speechRecord
            #print(speechrecord.date.cdata,speechrecord.speech.cdata)
            Reco += speechrecord.speech.cdata
        Reco += '\n'
        # w =カキコ,r =読み,a =追加カキコ,w+ =全部消してカキコ,r+ =既に書かれている内容を上書き,a+ =既に書かれている内容に追記
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(Reco)
        else:
            with open(path, 'a') as f:
                f.write(Reco)
        
        try:    #最後にエラーで終わるからここでにゃーん
            start = obj.data.nextRecordPosition.cdata
        except AttributeError:
            print("にゃーん")
            break
        
        i += 1
        print("取得ちう")
        #if i == 1:
        #    break
        
if __name__ == '__main__':
    path = "all_ABE_diet2018.csv"
    scrape(path)