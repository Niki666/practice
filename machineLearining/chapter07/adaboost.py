#coding:utf8
from numpy import *
def loadSimpData():
    datMat = matrix([[1. , 2.1],[2. , 1.1],[1.3 , 1.],[1. , 1.],[2. , 1.]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

#通过阈值进行比较对数据进行分类，通过数组过滤来实现
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray = ones((shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray

#遍历stumpClassify函数所有的可能输入值，并找到数据集上最佳的单层决策树
def buildStump(dataArr,classLabels,D):
    dataMatrix = mat(dataArr);labelMat = mat(classLabels).T  #确保输入数据符合矩阵格式
    m,n = shape(dataMatrix)
    #numSteps用于在所有特征让的所有可能值上进行遍历
    numSteps = 10.0;bestStump = {};bestClasEst = mat(zeros((m,1))) #bestStump这个字典用于存储给定权重向量D时所得到的最佳单层决策树的相关信息
    minError = inf  #初始化为正无穷大
    for i in range(n):
        rangeMin = dataMatrix[:,i].min();rangeMax = dataMatrix[:,i].max();stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt', 'gt']:
                threshVal = (rangeMin + float(j) * stepSize)
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal) #返回分类预测结果
                errArr = mat(ones((m,1))) #错误向量
                errArr[predictedVals == labelMat] = 0  #分类正确值置为0
                weightedError = D.T*errArr
                #print "split: dim %d,thresh %.2f, thresh inequal: %s, the weighted error is %.3f" %(i,threshVal,inequal,weightedError)
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClasEst

def adaBoostTrainDS(dataArr,classLabels,numIt = 40): #输入参数为数据集、类别标签和迭代次数
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)  #用来存储每个数据点的权重
    aggClassEst = mat(zeros((m,1)))  #记录每个点的类别估计累计值
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)  #首先建立一个单层决策树
        print "D:",D.T
        alpha = float(0.5*log((1.0-error)/max(error,1e-16)))  #单层决策树分类结果的权重
        bestStump['alpha'] = alpha   #alpha值加入到字典中，该字典包含了分类所需要的所有信息
        weakClassArr.append(bestStump)  #字典添加到列表中，
        print "classEst:",classEst.T
        expon = multiply(-1*alpha*mat(classLabels).T,classEst) #用于计算新权重
        D = multiply(D,exp(expon))
        D = D/D.sum()
        aggClassEst += alpha*classEst
        print"aggClassEst:",aggClassEst.T
        aggErrors = multiply(sign(aggClassEst)!=mat(classLabels).T,ones((m,1)))
        errorRate = aggErrors.sum()/m
        print "total error: ",errorRate,"\n"
        if errorRate == 0.0:
            break
    return weakClassArr


def adaClassify(datToClass,classifierArr):
    dataMatrix = mat(datToClass)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],classifierArr[i]['ineq'])
        aggClassEst += classifierArr[i]['alpha']*classEst
        print aggClassEst
    return sign(aggClassEst)


def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t'))
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(lineArr)
            labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

