# encoding: utf-8
#查询字典
# from recommendations import critics
# print critics['Lisa Rose']['Lady in the Water']
# print critics['Toby']['Snakes on a Plane']
# print critics['Toby']

#计算欧氏距离，其中pow(4.5-4, 2)pow(4.5-4, 2)是对某数求平方
# from math import sqrt
# print sqrt(pow(4.5-4, 2)+pow(1-2, 2))

# import recommendations
# reload(recommendations)
# movies=recommendations.transformPrefs(recommendations.critics)
#print recommendations.topMatches(movies,'Superman Returns')
#print recommendations.getRecommendations(movies,'Just My Luck')itemsim={}
# itemsim=recommendations.calculateSimilarItems(recommendations.critics)
# print itemsim

# print recommendations.getRecommendedItems(recommendations.critics,itemsim,'Toby')
# prefs=recommendations.loadMovieLens()
# print prefs['87']
#
# itemsim=recommendations.calculateSimilarItems(prefs,n=50)
# print recommendations.getRecommendedItems(prefs,itemsim,'87')[0:30]
#

import docclass
reload(docclass)
cl=docclass.classifier(docclass.getwords)
# cl.train('the quick brown fox jumps over the lazy dog','good')
# cl.train('make quick money in the online casino','bad')
# print cl.fcount('quick','good')
# print cl.fcount('quick','bad')
docclass.sampletrain(cl)
# print cl.fprob('quick','good')
# print cl.weightedprob('money','good',cl.fprob)
# docclass.sampletrain(cl)
print cl.weightedprob('money','good',cl.fprob)