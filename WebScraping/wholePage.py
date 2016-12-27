#encoding=utf-8
from urllib import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bs0bj = BeautifulSoup(html, "html.parser")
    try:
        print(bs0bj.h1.get_text())
        print(bs0bj.find(id="mw-content-text").findAll("p")[0])
        print(bs0bj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("页面却少一些属性，不过不用担心")
    for link in bs0bj.findAll("a", href = re.compile("^(/wiki/)")):
        if 'href'in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print("------------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")