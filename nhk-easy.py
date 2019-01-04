import requests
import sys
import json
import codecs
import os
import re
from bs4 import BeautifulSoup
from datetime import date


def main():

    r = requests.get('http://www3.nhk.or.jp/news/easy/news-list.json')
    r.encoding = 'utf-8-sig'
    o = json.loads(r.text)
    parse(o, '01')

def parse(o, mth):
    y = {}
    for k, v in o[0].items():
      regex = r'(\d+)' + r'(-+)' + re.escape(str(mth)) + r'(-\d+)'
      x = re.search(regex, k)
      if x:
        y[x.group()] = v
    parseMonth(y, mth)

def parseMonth(dic, mth):
    mth = str(mth)
    yr = ''.join(date.today().strftime("%Y-%m-%d").split('-')[0:1])
    join_str = yr + '_' + mth
    save_path = os.getcwd()
    output = save_path + '/' + join_str + '/' + join_str + '.html'
    folder = join_str

    if os.path.isdir(folder) == False:
        os.makedirs(folder)
        print("Directory \"" + folder + "/\" created")
    elif os.listdir(folder):
        print("Directory \"" + folder + "/\" exists!\n\nAbort.\n")
        return

    items = []
    content = []

    for k, v in dic.items():
        for i in v:
            item = parseNews(i)
            items.append(item)
            content.append(item["content"])
    
    content.reverse()

    with open(output, "w", encoding="utf-8") as f:
        print('<?xml version="1.0" encoding="UTF-8" ?>', file=f)
        print("<!DOCTYPE html>", file=f)
        print("<html lang='ja'>", file=f)
        print('<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" >', file=f)
        print('<style type="text/css">body { margin-left: 1em; margin-right: 1em; margin-top: 2em; margin-bottom: 2em; writing-mode:tb-rl; -epub-writing-mode: vertical-rl; -webkit-writing-mode: vertical-rl; line-break: normal; -epub-line-break: normal; -webkit-line-break: normal; color: #eee; font-size: larger; background: #111; line-height: 200%; font-family: "Hiragino Sans", sans-serif; } p { text-indent: 1em; font-size: medium } h1 { font-weight: bold; font-size: large; }</style>', file=f)
        print("</head>", file=f)
        print("<body>", file=f)
        print("<br />".join(content), file=f)
        print("</body>", file=f)
        print("</html>", file=f)
        print("File \"" + output + "\" created")
        
        file = open(save_path + '/' + join_str + '/' + join_str + '.opf', "w", encoding="utf-8")
        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><package version=\"3.0\" xmlns=\"http://www.idpf.org/2007/opf\"         unique-identifier=\"BookId\"> <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\"           xmlns:dcterms=\"http://purl.org/dc/terms/\">   <dc:title>NHK ニュース・読み物・" + join_str + "</dc:title>    <dc:contributor>NHK</dc:contributor>   <dc:language>ja</dc:language>   <dc:publisher>NHK</dc:publisher> </metadata> <manifest>  <item id=\"titlepage\" href=\"" + output + "\" media-type=\"application/xhtml+xml\" /> </manifest> <spine toc=\"tocncx\" page-progression-direction=\"rtl\">  <itemref idref=\"titlepage\" /> </spine></package>")
        print("File \"" + save_path + '/' + join_str + '/' + join_str + '.opf' + "\" created")
        file.close()
        
    print("The month's news were downloaded from NHK.")

def parseNews(news):
    news_id = news['news_id']
    news_time = news['news_prearranged_time'].replace(':', '-')
    title = news['title']
    title_ruby = news['title_with_ruby']
    news_uri = 'http://www3.nhk.or.jp/news/easy/' + str(news_id) + '/' + str(news_id) + '.html'

    r = requests.get(news_uri)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'html.parser')
    date = soup.find('p', attrs={'id':'js-article-date'})
    title = soup.find('h1', attrs={'class':'article-main__title'})#.find('h2')
    article = soup.find('div', attrs={'id':'js-article-body'})

    for a in article.findAll('a'):
        a.unwrap()
        voice = {}

    return {
        "content": str(title) + str(date) + str(article),
        "voice": voice
    }

main()
