#encoding=utf-8
from urllib import urlopen
from urlparse import *
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

#获取页面所有内链的列表
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

#获取页面所有外链的列表
def getExternalLinks(bs0bj,excludeUrl):
    externalLinks = []
    #找出所有以“http”或 "www"开头且不包含当前URL的链接
    for link in bs0bj.findAll("a",href = re.compile("^(/|.*"+excludeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in excludeUrl:
                externalLinks.append(link.attrs['href'])
    return externalLinks

#收集网站上发现的所有外链列表
allExtLinks = set()
allIntLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bs0bj = BeautifulSoup(html)
    internalLinks = getInternalLinks(bs0bj,splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bs0bj,splitAddress(siteUrl)[0])
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            print("即将获取链接的URL是："+link)
            allIntLinks.add(link)
            getAllExternalLinks(link)
getAllExternalLinks("http://oreilly.com")

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bs0bj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bs0bj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("No external links, looking around the site for one")
        domain = urlparse(startingPage).scheme+"://"+urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bs0bj,domain)
        return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0,len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is:"+externalLink)
    followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")
