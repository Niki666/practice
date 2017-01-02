#coding=utf-8
import urllib
import re
from bs4 import BeautifulSoup

path = 'http://www.cse.cqu.edu.cn'
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()

    return html

def getImg(html):
    bs0bj = BeautifulSoup(html,"html.parser")
    print bs0bj
    imglist = bs0bj.findAll("img",{"src":re.compile("\/teacherspic\/.*\.jpg")})
    print imglist
    x = 0
    for imgurl in imglist:
        url = path + imgurl['src'].encode('utf8')
        urllib.urlretrieve(url, '.\\%d.jpg' % x)
        x += 1
    return imglist


html = getHtml("http://www.cse.cqu.edu.cn/FrontPage/TeacherPage/")

print getImg(html)
