#coding:utf8
from numpy import *
def loadDataSet(filename):
    dataMat = [];labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m): #i是alpha的下标，m是alpha的数目，只要函数值不等于输入值i，函数就会进行随机选择
    j = i
    while (j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L): #用于调整大于H或小于L的alpha值
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter): #数据集、类别标签、常数C、容错率、退出前最大的循环次数
    dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose() #转换为numpy矩阵，将类别标签转置得到列向量
    b = 0;m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1))) #构建m行1列alpha列矩阵并将所有元素初始化为0
    iter = 0  #存储在没有任何alpha改变的情况下遍历数据集的次数
    while (iter < maxIter):   #若iter大于最大值则终止
        alphaPairsChanged = 0  #用于记录alpha是否优化，每次循环前先将alphaPairsChanged设置为0，然后再对整个集合顺序遍历
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T))+b #预测的类别
            Ei = fXi - float(labelMat[i])  #误差
            #若误差大于容错率，则优化alpha值
            if ((labelMat[i] < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler)and (alphas[i] > 0)):
                j = selectJrand(i,m)  #随机选择第二个alpha值
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                Ej = fXj - float(labelMat[j])  #计算选择的alpha值得误差
                alphaIold = alphas[i].copy();
                alphaJold = alphas[j].copy();
                if (labelMat[i] != labelMat[j]):  #LH用于将alpha[j]的值调整到0C之间
                    L = max(0,alphas[j]-alphas[i])
                    H = min(C, C+alphas[j]-alphas[i])
                else:
                    L = max(0,alphas[j]+alphas[i]-C)
                    H = min(C,alphas[j]+alphas[i])
                if L==H:
                    print"L==H";continue  #本次循环结束，直接运行下一次for循环
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0:  #eta是alpha[j]的最优修改量
                    print "eta >= 0";continue
                alphas[j] -= labelMat[j]*(Ei-Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H, L)
                if (abs(alphas[j]-alphaJold)<0.00001): #检查alphas[j]是否有轻微改变，如果是，则退出循环
                    print"j not moving enough";continue
                #alphas[i]alphas[j]同时修改，修改量相同，方向相反
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T -labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T
                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1+b2)/2.0
                alphaPairsChanged += 1
                print "iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
        if (alphaPairsChanged == 0):
            iter += 1
        else:
            iter = 0
        print "iteration number: %d" % iter
    return b,alphas

class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m, 1)))
        self.b = 0
        self.eCache = mat(zeros((self.m, 2)))

    def calcEk(oS, k):
        fXk = float(multiply(oS.alphas,oS.labelMat).T*(oS.X*oS.X[k,:].T)) + oS.b
        Ek = fXk - float(oS.labelMat[k])
        return Ek

    def selectJ(i, oS, Ei):
        maxK = -1;maxDeltaE = 0;Ej = 0
        oS.eCache[i] = [1,Ei]
        validEcacheList = nonzero(oS.eCache[:,0].A)[0]
        if (len(validEcacheList)) > 1:
            for k in validEcacheList:
                if k == i:
                    continue
                Ek = calcEk(oS, k)
                deltaE = abs(Ei - Ek)
                if (deltaE > maxDeltaE):
                    maxK = k; maxDeltaE = deltaE; Ej = Ek
            return maxK, Ej
        else:
            j = selectJrand(i, oS.m)
            Ej = calcEk(oS, j)
        return j, Ej

    def updateEk(oS, k):
        Ek = calcEk(oS, k)
        oS.eCache[k] = [1,Ek]