# encoding: utf-8

# import urllib2
# c=urllib2.urlopen('https://www.baidu.com/')
# contents=c.read()
# print contents[0:50]

import searchengine
pagelist=['http://kiwitobes.com/wiki/Perl.html']
crawler=searchengine.crawler('')
crawler.crawl(pagelist)
reload(searchengine)
crawler=searchengine.crawler('searchindex.db')
crawler.createindextables()