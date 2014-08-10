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
        response = urllib2.urlopen(url)
        html = response.read()
        response.close()
        soup = BeautifulSoup(html)
        return "- [{0}]({1})".format(soup.html.head.title.contents[0], url)
    except urllib2.URLError, e:
        return False
    except urllib2.HTTPError, e:
        return False
    except:
        return False



handler = Alfred.Handler(args=sys.argv)
result = getUrl(handler.query.split(" ")[1])

if not result:
    handler.add_new_item(title="No find WebPage:(")
else:
    handler.add_new_item(title=result, arg=result, uid="#1")

handler.push(max_results=1)

# if __name__ == '__main__':
#     getUrl(query)







