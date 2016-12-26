import adaboost
from numpy import *
datArr, labelArr = adaboost.loadDataSet('horseColicTest2.txt')
classifierArray = adaboost.adaBoostTrainDS(datArr,labelArr,30)
# print classifierArray
# reload(adaboost)
# adaboost.adaClassify([[5,5],[0,0]],classifierArr)
