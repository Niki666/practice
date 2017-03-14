#coding:utf-8
import numpy as np
class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = np.shape(dataMatIn)[0]
        self.alphas = np.mat(np.zeros((self.m,1)))
        self.b = 0
        self.eCache = np.mat(np.zeros((self.m,2)))

def loadDataSet(fileName):
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

#误差缓存
def calcEk(oS,k):
    fXk = float(np.multiply(oS.alphas,oS.labelMat).T*(oS.X*oS.X[k,:].T)) + oS.b
    Ek = fXk - float(oS.labelMat[k])
    return Ek

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

# 用于选择第二个alpha值（内循环的alpha值）
def selectJ(i,oS,Ei):
    maxK = -1; maxDeltaE = 0; Ej = 0
    oS.eCache[i] = [1,Ei]
    validEcacheList = np.nonzero(oS.eCache[:,0].A)[0]  #nonzero返回的是非零E值所对应的alpha值
    if (len(validEcacheList))>1:
        for k in validEcacheList:
            if k == i:
                continue
            Ek = calcEk(oS,k)
            deltaE = abs(Ei-Ek)
            #选择具有最大步长的J
            if (deltaE>maxDeltaE):
                maxK = k; maxDeltaE = deltaE; Ej = Ek
        return  maxK,Ej
    else:
        j = selectJrand(i,oS.m)
        Ej = calcEk(oS,j)
    return j, Ej

#计算误差并存入缓存，在对alpha优化之后会用到这个值
def updateEk(oS,k):
    Ek = calcEk(oS,k)
    oS.eCache[k] = [1,Ek]

#优化历程
def innerL(i,oS):
    Ei = calcEk(oS,i)
    if ((oS.labelMat[i] * Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i] * Ei > -oS.tol) and (oS.alphas[i] > 0)):
        j,Ej = selectJ(i,oS,Ei)
        alphaIold = oS.alphas[i].copy()
        alphaJold = oS.alphas[j].copy()
        if (oS.labelMat[i] != oS.labelMat[j]):
            # 计算L\H 用于将alpha调整到0，C之间
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L == H:
            print "L == H"
            return 0
        # eta是alpha[j]的最优修改量
        eta = 2.0 * oS.X[i, :] * oS.X[j, :].T - oS.X[i, :] * oS.X[i, :].T - oS.X[j,:] * oS.X[j,:].T
        if eta >= 0:
            print "eta>=0"
            return 0
        oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej) / eta
        oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
        if (abs(oS.alphas[j] - alphaJold) < 0.00001):
            print "j not moving enough"
            return 0
        oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i] * (alphaJold - oS.alphas[j])
        b1 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.X[i, :] * oS.X[i, :].T - oS.labelMat[j] * (
        oS.alphas[j] - alphaJold) * oS.X[i, :] * oS.X[j, :].T
        b2 = oS.b - Ei - oS.labelMat[i] * (oS.alphas[i] - alphaIold) * oS.X[i, :] * oS.X[j, :].T - oS.labelMat[j] * (
        oS.alphas[j] - alphaJold) * oS.X[j, :] * oS.X[j, :].T
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]):
            oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]):
            oS.b = b2
        else:
            oS.b = (b1 + b2) / 2.0
        return 1
    else:
        return 0

#外循环代码
def smoP(dataMatIn,classLabels,C,toler,maxIter,kTup=('lin',0)):
    oS = optStruct(np.mat(dataMatIn),np.mat(classLabels).transpose(),C,toler)
    iter = 0
    entireSet = True; alphaPairsChanged = 0
    while (iter<maxIter) and ((alphaPairsChanged > 0)or(entireSet)):
        alphaPairsChanged = 0
        if entireSet:
            for i in range(oS.m):
                alphaPairsChanged += innerL(i,oS)
                print "fullSet,iter:%d i:%d,pairs changed %d"%(iter,i,alphaPairsChanged)
            iter += 1
        else:
            nonBoundIs = np.nonzero((oS.alphas.A>0)*(oS.alphas.A<C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i,oS)
                print "non-bound,iter:%d i:%d, pairs changed %d"%(iter,i,alphaPairsChanged)
            iter += 1
        if entireSet:entireSet = False
        elif(alphaPairsChanged == 0):
            entireSet = True
            print"interation number:%d" % iter
        return oS.b ,oS.alphas

dataArr,labelArr = loadDataSet('testSet.txt')
b,alphas = smoP(dataArr,labelArr,0.6,0.001,40)
print b

