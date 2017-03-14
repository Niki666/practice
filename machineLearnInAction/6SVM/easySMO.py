#coding:utf-8
import numpy as np
#SMO算法中的辅助函数
def loadDataSet(fileName):
    dataMat = [];  labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m):
    # we want to select any J not equal to i
    j = i  #i是第一个alpha的下标，m是所有alpha的数目
    while (j==i):  #只要函数值不等于输入值i，函数就会随机进行选择
        j = int(np.random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    #用于调整大于H或者小于L的alpha的是值
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn,classLables,C,toler,maxIter): #数据集、类别标签、常数C、容错率和推出前最大的错误标签
    dataMatrix = np.mat(dataMatIn); labelMat = np.mat(classLables).transpose()
    b = 0; m,n = np.shape(dataMatrix)
    alphas = np.mat(np.zeros((m,1)))  #初始化列中元素为0
    iter = 0  #存储在没有alpha改变的情况下遍历数据集的次数
    while (iter < maxIter):
        alphaPairsChanged = 0  #用于记录alpha是否已经进行优化
        for i in range(m):
            fXi = float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T))+b  #fXi位预测的类别
            Ei = fXi - float(labelMat[i]) #计算误差
            #如果误差大于容错率，则优化alpha
            if ((labelMat[i]*Ei < -toler) and (alphas[i]<C))or((labelMat[i]*Ei>toler)and(alphas[i]>0)):
                j = selectJrand(i,m)
                fXj = float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T))+b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if (labelMat[i] != labelMat[j]):
                    #计算L\H 用于将alpha调整到0，C之间
                    L = max(0,alphas[j]-alphas[i])
                    H = min(C,C + alphas[j]-alphas[i])
                else:
                    L = max(0,alphas[j]+alphas[i]-C)
                    H = min(C,alphas[j]+alphas[i])
                if  L == H:
                    print "L == H"
                    continue
                #eta是alpha[j]的最优修改量
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0:
                    print "eta>=0"
                    continue
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                if (abs(alphas[j]-alphaJold)<0.00001):
                    print "j not moving enough"
                    continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i]-alphaIold)* dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ei - labelMat[i]*(alphas[i]-alphaIold)* dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0<alphas[i])and(C>alphas[i]):
                    b = b1
                elif(0<alphas[j])and(C>alphas[j]):
                    b = b2
                else:
                    b = (b1+b2)/2.0
                    alphaPairsChanged += 1
                    print "iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
        if (alphaPairsChanged ==0):
            iter += 1
        else:
            iter = 0
        print "iteration number:%d" % iter
    return b,alphas
dataArr,labelArr = loadDataSet('testSet.txt')
b,alphas = smoSimple(dataArr,labelArr,0.6,0.001,40)
print b
print alphas[alphas>0]