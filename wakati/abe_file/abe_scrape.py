import urllib
import untangle
import urllib.parse
from bs4 import BeautifulSoup

if __name__ == '__main__':
    start = '1'
    i = 0
    while start != None:
        keyword = '安倍晋三'
        startdate = '2018-01-01'
        enddate = '2018-12-31'
        #meeting = '予算委員会'
        #urllib.parse.quoteが日本語をコーディングしてくれる
        url = 'http://kokkai.ndl.go.jp/api/1.0/speech?'+urllib.parse.quote('startRecord=' + start
                                                                           #+ '&maximumRecords=100&speaker=' + keyword
                                                                           #+ '&nameOfMeeting=' + meeting
                                                                           + '&from=' + startdate
                                                                           + '&until=' + enddate)
        obj = untangle.parse(url)
        #print(obj.data.numberOfRecords.cdata, type(obj.data.records.record))
        for record in obj.data.records.record:
            speechrecord = record.recordData.speechRecord
            #print(speechrecord.date.cdata,speechrecord.speech.cdata)

            # w =カキコ,r =読み,a =追加カキコ,w+ =全部消してカキコ,r+ =既に書かれている内容を上書き,a+ =既に書かれている内容に追記
            with open('2018kokkai.txt', 'a') as f:
                f.write(speechrecord.speech.cdata)

        try:    #最後にエラー出るのが気に食わないので例外処理にしてみたｗ
            start = obj.data.nextRecordPosition.cdata
        except AttributeError:
            print("にゃーん")
            break
        i += 1
        print(i)
        #if i == 1:
        #    break
        