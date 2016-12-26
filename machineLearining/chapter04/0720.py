#coding:utf8
import bayes
import feedparser
from numpy import *
reload(bayes)
# listOPosts,listClasses = bayes.loadDataSet()
# myVocabList = bayes.createVocabList(listOPosts)
# print myVocabList
# print bayes.setOfWords2Vec(myVocabList,listOPosts[3])
# trainMat = []
# for postinDoc in listOPosts:
#     trainMat.append(bayes.setOfWords2Vec(myVocabList, postinDoc))
# p0V,p1V,pAb = bayes.trainNB0(trainMat,listClasses)
# print pAb
# print p0V
# print p1V
#
# print bayes.spamTest()
ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
# vocabList,pSF,pNY = bayes.localWords(ny,sf)
print bayes.getTopWords(ny,sf)