#coding:utf8
# import work
# trainSet,trainLabel=work.training()
# testSet=work.testing()
# testLabel = []
# for line in testSet:
#     testLabels = work.classify0(line,trainSet,trainLabel,5)
#     testLabel.append(testLabels)
# print testLabel

import KNN
from numpy import array
import matplotlib
import matplotlib.pyplot as plt
reload(KNN)
# datingDataMat,datingLabels = KNN.file2matrix('datingTestSet2.txt')
#print datingDataMat,datingLabels
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(datingDataMat[:,1], datingDataMat[:, 2],15.0*array(datingLabels), 15.0*array(datingLabels))
# plt.show()
# normMat, ranges, minVals = KNN.autoNorm(datingDataMat)
# print normMat, ranges, minVals
# print KNN.datingClassTest()
# print KNN.classifyPerson()
# testVector = KNN.img2vector('testDigits/0_13.txt')
# print testVector[0,0:31]
print KNN.handwritingClassTest()