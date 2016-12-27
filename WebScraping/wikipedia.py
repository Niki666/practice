from urllib import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

# html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
# bs0bj = BeautifulSoup(html,"html.parser")
# for link in bs0bj.find("div",{"id":"bodyContent"}).findAll("a",href = re.compile("^(/wiki/)((?!:).)*$")):
#     if 'href' in link.attrs:
#         print(link.attrs['href'])

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bs0bj = BeautifulSoup(html,"html.parser")
    return bs0bj.find("div",{"id":"bodyContent"}).findAll("a",href = re.compile("^(/wiki/)((?!:).)*$"))
links = getLinks("/wiki/Kevin_Bacon")
while len(links)>0:
    newArticle = links[random.randint(0,len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
