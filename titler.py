# -*- coding: utf-8 -*-
import urllib2,Alfred,sys;
from bs4 import BeautifulSoup

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
        response.close()
        soup = BeautifulSoup(html)
        return "- [{0}]({1})".format(soup.title.contents[0].strip(), response.geturl())
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

if not result:
    handler.add_new_item(title="No find WebPage:(")
else:
    handler.add_new_item(title=result, arg=result, uid="#1")

handler.push(max_results=1)











