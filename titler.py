# -*- coding: utf-8 -*-
import urllib2,Alfred,sys;
from bs4 import BeautifulSoup
from chardet import *

# query = sys.argv[1]

def fixCoding():
    sysEncoding = sys.getdefaultencoding()
    if sysEncoding != 'UTF-8':
        reload(sys)
        sys.setdefaultencoding('UTF-8')
fixCoding()

def getUrl(url):
    try:
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        response = urllib2.urlopen(req)
        html = response.read()
        # chardetdict=chardet.detect(html)
        # if chardetdict.get('encoding')=='Big5':
        #     html=html.decode('big5','ignore').encode('utf-8','ignore')
        response.close()
        soup = BeautifulSoup(html)
        title = soup.title.contents[0].strip()
        return "- [{0}]({1})".format(title, response.geturl())
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

if not result:
    handler.add_new_item(title="No find WebPage:(")
else:
    handler.add_new_item(title=result, arg=result, uid="#1")

handler.push(max_results=1)











