#coding:utf8
from numpy import *
#从文本中构建词向量
import feedparser
def loadDataSet():
    postingList=[['my','dog','has','flea','problem','help','please'],
                 ['maybe','not','take','him','to','dog','park','stupid'],
                 ['my','dalmation','is','so','cute','I','love','him'],
                 ['stop','posting','stupid','worthless','garbage'],
                 ['mr','licks','ate','my','steak','how','to','stop','him'],
                 ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1]
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])  #创建一个空集 set构造函数会返回一个不重复词表
    for document in dataSet:
        vocabSet = vocabSet | set(document) #创建两个集合的并集 “|”求两个集合的并集
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):  #该函数输入词汇表或文档，输出文档向量
    returnVec = [0]*len(vocabList)  #创建一个和词汇表等长的向量，并将其元素都设置为0
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1 #出现向量为1
        else:
            print "the word: %s is not in mu Vocabulary!" % word
    return returnVec

#从词向量计算概率
#朴素贝叶斯分类器训练函数
def trainNB0(trainMatrix,trainCategory): #输入文档矩阵，由每篇文档类别标签所构成的向量
    numTrainDocs = len(trainMatrix)  #矩阵行数
    numWords = len(trainMatrix[0])   #矩阵列数
    pAbusive = sum(trainCategory)/float(numTrainDocs) #任意文档属于侮辱性文档的概率，因为是0,1，所以直接用1的和除以长度
    p0Num = ones(numWords);p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i]) #每一行词向量中出现词汇的和相加得到侮辱性的词条中所有的词汇
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)   #change to log()
    p0Vect = log(p0Num/p0Denom)   #change to log()
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts) #去除重复词
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))  #向量化
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love','my','dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['stupid','garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

def bagOfWords2VecMN(vocabList,inputSet):  #该函数输入词汇表或文档，输出文档向量
    returnVec = [0]*len(vocabList)  #创建一个和词汇表等长的向量，并将其元素都设置为0
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1 #出现向量为1
        else:
            print "the word: %s is not in mu Vocabulary!" % word
    return returnVec

#准备数据，切分文本
#接受一个大字符串并将其解析为字符串列表，该函数去掉少于两个字符的字符串，并转换为小写
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\w',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

#对贝叶斯垃圾邮件分类器进行自动化处理
def spamTest():
    docList = [];classList = [];fullText = []
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())  #导入文件并将其解析为词列表
        docList.append(wordList)  #append()接受一个对象参数，把对象添加到列表的尾部
        fullText.extend(wordList) #extend()接受一个列表参数，把参数列表的元素添加到列表的尾部
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)  # append()接受一个对象参数，把对象添加到列表的尾部
        fullText.extend(wordList)  # extend()接受一个列表参数，把参数列表的元素添加到列表的尾部
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50);testSet = []  #构建10测试集和50训练集
    for i in range(10):
        randIndex = int (random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex]) #将随机选出的数据加入测试集
        del(trainingSet[randIndex]) #从训练集中将该数据删除
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[docIndex]) #词向量
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)

#从广告获取区域倾向
#RSS源分类器及高频词去除函数 遍历词汇表中的每个词并统计它在文本中出现的次数，
#然后根据出现次数从高到低对词典进行排序
def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token) #???
    sortedFreq = sorted(freqDict.iteritems(), key = operator.itemgetter(1), reverse=True) #???
    return sortedFreq[:30]

def localWords(feed1,feed0):
    import feedparser
    docList = [];classList = []; fullText = []
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30words = calcMostFreq(vocabList,fullText)
    for pairW in top30words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])  #将出现频率最高的词汇移除
    trainingSet = range(2*minLen); testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = [];trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V

#最具表征性的词汇显示函数
def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V = localWords(ny,sf)
    topNY = []; topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -0.6 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -0.6 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key = lambda pair: pair[1], reverse=True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key = lambda pair: pair[1], reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]
        