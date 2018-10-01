import os
import urllib
import json
from bs4 import BeautifulSoup

def search(keyword,maximum):
    if not os.path.exists(keyword):
        os.mkdir(keyword)
    urlKeyword = urllib.parse.quote(keyword)    #url用に
    url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}  #偽装
    request = urllib.request.Request(url=url, headers=headers) 
    page = urllib.request.urlopen(request)  #おーぷん
    html = page.read().decode("utf8")  #判定をもとにデコード
    html = BeautifulSoup(html, "html.parser")
    elems = html.select('.rg_meta.notranslate')
    jsons = [json.loads(e.get_text()) for e in elems]
    imageURLs = [js['ou'] for js in jsons]  #一度に100件までしか持ってこれないっぽい
    result = []
    count = 0
    print(imageURLs)
    """
    while len(imageURLs):
        if not len(imageURLs):
            print('-> no more images')
            break
        elif len(imageURLs) > maximum - count:
            result += imageURLs[:maximum - count]
            break
        else:
            result += imageURLs
            count += len(imageURLs)
    """

if __name__ == '__main__':
    keyword = "あ"#input("画像検索：")
    maximum = 1#int(input("何枚？"))
    search(keyword,maximum)
