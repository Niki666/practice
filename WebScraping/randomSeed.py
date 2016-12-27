from urllib import urlopen
from urlparse import *
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

def getInternalLinks(bs0bj,includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"//"+urlparse(includeUrl).netloc
    internalLinks = []
    for link in bs0bj.findAll("a",href = re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

