#coding:utf-8
#author:fangqianqi
#2017-03-15
import numpy as np
#基于单层决策树构建弱分类器
def loadSimpData():
    datMat = np.matrix([[1.,2.1],[2.,1.1],[1.3,1.],[1.,1.],[2.,1.]])
    classLabels = [1.0,1.0,-1.0,-1.0,1.0]
    return datMat,classLabels

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) #get number of fields
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

#自适应加载数据
def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t'))
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat - 1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat


def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):
    retArray = np.ones((np.shape(dataMatrix)[0],1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen]<=threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen]>threshVal] = -1.0
    return retArray

#单层决策树生成函数
#1.将最小错误率minError设为无穷大
#2.对数据集中每一个特征（第一层循环）：
#3.    对每个步长（第二层循环）：
#4.        对每个不等号（第三层循环）：
#              建立一棵单层决策树并利用加权数据集对它进行测试
#              如果错误率低于minError，则将当前单层决策树设为最佳单层决策树
def buildStump(dataArray,classLabels,D):
    dataMatrix = np.mat(dataArray)
    labelMat = np.mat(classLabels).T
    m,n = np.shape(dataMatrix)
    numSteps = 10.0
    bestStump = {} #this dict used to store the beat tree of the D
    bestClassEst = np.mat(np.zeros((m,1)))
    minError = np.inf  #开始被设为无穷大，后面用来寻找可能的最小错误率
    for i in range(n):
        rangeMin = dataMatrix[:,i].min()
        rangeMax = dataMatrix[:,i].max()
        stepSize = (rangeMax - rangeMin)/numSteps  #计算步长
        for j in range(-1,int(numSteps)+1):
            for inequal in ['lt','gt']:
                threshVal = (rangeMin+float(j)*stepSize)
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)
                errArr = np.mat(np.ones((m,1)))
                errArr[predictedVals == labelMat] = 0
                weightedError =D.T*errArr  #D为权重向量
                #print"split:dim %d,thresh %.2f, thresh inequal: %s, the weighted error is %.3f"%(i,threshVal,inequal,weightedError)
                if weightedError < minError:
                    minError = weightedError
                    bestClassEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClassEst

#利用buildStump()函数找到最佳的单层决策树
#将最佳单层决策树加入到单层决策树组
#计算alpha
#计算新的权重向量D
#更新累计类别估计值
#如果错误率等于0.0，则退出循环

#基于单层决策树的AdaBoost训练过程
def adaBoostTrainDS(dataArr,classLabels,numIt=40): #数据集、类别标签、迭代次数
    weakClassArr = []
    m = np.shape(dataArr)[0]
    D = np.mat(np.ones((m,1))/m)
    aggClassEst = np.mat(np.zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)
        print"D:",D.T
        alpha = float(0.5*np.log((1.0-error)/max(error,1e-16)))
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print "ClassEst: ",classEst.T
        expon = np.multiply(-1*alpha*np.mat(classLabels).T,classEst)
        D = np.multiply(D,np.exp(expon))
        D = D/D.sum()
        aggClassEst += alpha*classEst
        print "aggClassEst: ",aggClassEst.T
        aggErrors = np.multiply(np.sign(aggClassEst) != np.mat(classLabels).T, np.ones((m,1)))
        errorRate = aggErrors.sum()/m
        print"toler error: ",errorRate,"\n"
        if errorRate == 0.0:
            break
    return weakClassArr,aggClassEst

#AdaBoost分类函数
def adaClassify(datToClass,classifierArr):
    dataMatrix = np.mat(datToClass)
    m = np.shape(dataMatrix)[0]
    aggClassEst = np.mat(np.zeros((m,1)))
    for i in range(len(classifierArray)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],classifierArr[i]['ineq'])
        aggClassEst+=classifierArr[i]['alpha']*classEst
        print aggClassEst
    return np.sign(aggClassEst)

#ROC曲线的绘制及AUC计算函数
def plotROC(predStrengths,classLabels):
    import matplotlib.pyplot as plt
    cur = (1.0,1.0)  #该元祖保留的是绘制光标的位置
    ySum = 0.0 #用于计算AUC的值
    numPosClas = sum(np.array(classLabels)==1.0)  #数组过滤计算正类数目
    yStep = 1/float(numPosClas)  #y轴步长
    xStep = 1/float(len(classLabels)-numPosClas)
    sortedIndicies = predStrengths.argsort()  #索引排序
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    for index in sortedIndicies.tolist()[0]:  #Return the array as a (possibly nested) list
        if classLabels[index] == 1.0:
            delX = 0
            delY = yStep
        else:
            delX = xStep
            delY = 0
            ySum += cur[1]
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY],c='b')
        cur = (cur[0]-delX,cur[1]-delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve for AdaBoost Horse Colic Detection System')
    ax.axis([0,1,0,1])
    plt.show()
    print "the Area Under the Curver is: ",ySum*xStep

datArr,labeLArr = loadDataSet('horseColicTraining2.txt')
classifierArray,aggClassEst = adaBoostTrainDS(datArr,labeLArr,10)
plotROC(aggClassEst.T,labeLArr)


