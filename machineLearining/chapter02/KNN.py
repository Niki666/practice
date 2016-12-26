#coding:utf8
from numpy import *
import operator
from os import listdir

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group, labels

#算法核心
#inX：用于分类的输入向量。即将对其进行分类。
#dataSet：训练样本集
#labels:标签向量
def classify0(inX, dataSet, Labels, k):
    dataSetSize=dataSet.shape[0] #得到数组的行数。即知道有几个训练数据
    #tile:numpy中的函数。tile将原来的一个数组，扩充成了4个一样的数组。diffMat得到了目标与训练数值之间的差值。
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat=diffMat**2 #各个元素分别平方
    sqDistances=sqDiffMat.sum(axis=1) #我们平时用的sum应该是默认的axis=0 就是普通的相加,
    # 而当加入axis=1以后就是将一个矩阵的每一行向量相加:x**2+y**2
    distances=sqDistances**0.5  #开方，得到距离
    sortedDistIndicies=distances.argsort() #升序排列
    #选择距离最小的K个点
    classCount = {}
    for i in range(k):
        voteIlabel = Labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1 #classCount.get 从字典中取值，key为voteIlabel，如果没有返回0，如果有就加1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines, 3))  #zeros创建n行3列的矩阵，值均为0
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]   #选取前3个元素存储到特征矩阵
        classLabelVector.append(int(listFromLine[-1]))  #-1表示最后一列元素，如果不用int(),将当做字符串处理
        index += 1
    return returnMat,classLabelVector

#归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0) #存放每一列的最小值，min(0)参数0可以从列中选取最小值，而不是当前行最小值
    maxVals = dataSet.max(0) #存放每一列的最大值
    ranges = maxVals - minVals   #1 * 3 矩阵
    normDataSet = zeros(shape(dataSet))  #列
    m = dataSet.shape[0]   #行
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet, ranges, minVals

#测试准确率
def datingClassTest():
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],4)
        print "the classifier came back with:%d, the real answer is:%d"%(classifierResult,datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print "the total error rate is : %f" % (errorCount/float(numTestVecs))

#约会网站预测函数
def classifyPerson():
    resultList = ['not at all','in small does','in large does']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year"))
    iceCream = float(raw_input("liters of ice cream consumed per year"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0(inArr-minVals ,normMat,datingLabels,3)
    print " You will probably like this person:",resultList[classifierResult - 1]

#手写识别示例
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

#手写识别系统的测试代码
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits') #listdir是一个函数，列出给定目录的文件名
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]  #去掉后缀
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i:1] = img2vector('trainingDigits/%s'%fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]  # 去掉后缀
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print "the classifier came back with : %d,the real answer is: %d" %(classifierResult,classNumStr)
        if (classifierResult != classNumStr):
            errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %d" % (errorCount/float(mTest))