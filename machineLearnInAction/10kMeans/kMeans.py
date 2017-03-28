#coding:utf-8
#author:fangqianqi
#date:2017-03-16
from numpy import *

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)  #map(f, iterable)=[f(x) for x in iterable]
        dataMat.append(fltLine)
    return dataMat

#计算欧氏距离
def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA-vecB,2)))

#为给定数据集构建一个人包含k个随机质心的集合
def randCent(dataSet,k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])   #j is col
        rangeJ = float(max(dataSet[:,j]) - minJ)   #求坐标边界
        centroids[:,j] = minJ + rangeJ*random.rand(k,1)
    return centroids

#k均值聚类算法
def kMeans(dataSet,k,distMeas=distEclud,createCent = randCent):
    #:param dataSet: 数据集，要求有矩阵形式
    #:param k: 指定聚类的个数
    #:param disMens: 求解距离的方式，除欧式距离还可以定义其他距离计算方式
    #:param createCent: 生成随机质心方式
    #:return:随机质心，簇索引和误差距离矩阵
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centorids = createCent(dataSet,k) #构建k个质心
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centorids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i,0]  != minIndex:
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centorids
        #遍历所有的质心并更新
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            # nonzero 返回的是矩阵中所有非零元素的坐标，坐标的行数与列数个存在一个数组或矩阵当中
            # 矩阵支持检查元素的操作，所有可以写成matrix == int这种形式，返回的一个布尔型矩阵，代表矩阵相应位置有无此元素
            # 这里指寻找当前质心下所聚类的样本
            centorids[cent,:] = mean(ptsInClust,axis=0)
            # 更新当前的质心为所有样本的平均值，axis = 0代表对列求平均值
    return centorids,clusterAssment


#二分K-均值方法
#将所有点看成一个簇
#当簇数目小于K时
#    对于每一个簇
#       计算总误差
#       在给定的簇上面进行K-均值聚类(k=2)
#       计算将该簇一分为二后的总误差
#   选择是的误差最小的那个簇进行划分操作

def biKmeans(dataSet,k,distMeas=distEclud):
    #:param dataSet: 数据集，要求有矩阵形式
    #:param k: 指定聚类个数
    #:param distMeas: 求解距离的方式
    #return:质心，簇索引和误差距离矩阵
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2))) #存储数据集中每个点的簇分配结果及平方误差mx2矩阵
    centroid0 = mean(dataSet,axis=0).tolist()[0] #计算整个簇的质心
    centList = [centroid0]   #列表存储质心
    for j in range(m):
        clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2  #计算数据到质心的欧氏距离
    while (len(centList)<k):
        lowestSSE = inf
        for i in range(len(centList)):
            # 搜索到当前质心所聚类的样本
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]  #nonzeros()返回输入值中非零元素的信息（以矩阵的形式）.A表示转置
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster,2,distMeas)   # 将当前分割成两个簇
            sseSplit = sum(splitClustAss[:,1])   # 计算分裂簇后的SSE
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])  # 计算分裂之前的SSE
            print"sseSplit,and notSplit:",sseSplit,sseNotSplit
            if (sseSplit+sseNotSplit)<lowestSSE:   # 如果分裂之后的SSE小，则更新
                bestCentToSplit = i
                bestNewcents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0]=len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print 'the bestCentToSplit is :',bestCentToSplit
        print 'the len of beatClustAss is :',len(bestClustAss)
        centList[bestCentToSplit]=bestNewcents[0,:]
        centList.append(bestNewcents[1,:])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]=bestClustAss
    return mat(centList),clusterAssment


datMat3 = mat(loadDataSet('testSet2.txt'))
cenList,myNewAssments = biKmeans(datMat3,3)