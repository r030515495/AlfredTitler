# -*- coding: utf-8 -*-
import urllib2
import Alfred
import sys
import re

from bs4 import BeautifulSoup
from xml.sax.saxutils import escape
# query = sys.argv[1]

def fixCoding():
    sysEncoding = sys.getdefaultencoding()
    if sysEncoding != 'UTF-8':
        reload(sys)
        sys.setdefaultencoding('UTF-8')
fixCoding()


def decodeUrl(q):
    '''
    get url by  format
    [{title}]{url}
    - [{title}]({url})
    '''
    match = re.match(r"-{0,1}\s{0,1}\[(?P<title>.*)\]\({0,1}(?P<url>[^\)]*)\){0,1}",q)
    if match:
        return match.group("url")
    else :
        return q

def getUrl(url):
    try:
        url = decodeUrl(url)
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
        soup = BeautifulSoup(html)
        title = escape(soup.title.contents[0].strip())
        if  title:
            result = [];
            result.append("[{0}]{1}".format(title, response.geturl()));
            result.append("- [{0}]({1})".format(title, response.geturl()));
            return result;
        else:
            return False;
    except urllib2.URLError, e:
        return False
    except urllib2.HTTPError, e:
        return False
    except:
        return False



handler = Alfred.Handler(args=sys.argv)
result = getUrl(handler.query)

# test
# not have html tag
# result = getUrl("http://learn.getchef.com/")
# title 遇到big5 網頁亂碼
# result = getUrl("http://www2.nsysu.edu.tw/csmlab/unix/vi_command.htm")
# need escape page
# result = getUrl("http://jex.im/regulex/")
# 解析我自己產出的格式
# result = getUrl("[讓你快速搜尋 Facebook 塗鴉牆內容——QSearch 團隊專訪 - Inside 硬塞的網路趨勢觀察]http://www.inside.com.tw/2013/02/19/qsearch-interview")
# result = getUrl("- [讓你快速搜尋 Facebook 塗鴉牆內容——QSearch 團隊專訪 - Inside 硬塞的網路趨勢觀察](http://www.inside.com.tw/2013/02/19/qsearch-interview)")

if not result:
    handler.add_new_item(title="No find WebPage:(")
else:
    for key in result:
        handler.add_new_item(title=key, arg=key, uid="#1")

handler.push(max_results=2)











