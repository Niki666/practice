from urllib import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs0bj = BeautifulSoup(html,"html.parser")

#children()
# for child in bs0bj.find("table",{"id":"giftList"}).children:
#     print(child)

#next_siblings()
# for sibling in bs0bj.find("table",{"id":"giftList"}).tr.next_siblings:
#     print(sibling)

#parent
# print(bs0bj.find("img",{"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())

#find image
images = bs0bj.findAll("img",{"src":re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
for image in images:
    print(image["src"])