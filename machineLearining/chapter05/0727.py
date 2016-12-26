#coding:utf8
import logRegres
from numpy import *
dataArr, labelMat = logRegres.loadDataSet()
# print logRegres.gradAscent(dataArr,labelMat)
reload(logRegres)
# weights = logRegres.stocGradAscent1(array(dataArr),labelMat)
# logRegres.plotBestFit(weights)
print logRegres.multiTest()

