#coding:utf8
import trees
reload(trees)
myDat,labels = trees.createDataSet()
# myDat[0][-1] = 'maybe' #list中第一个元素中最后一个元素的值改变
# print myDat
# print trees.splitDataSet(myDat,0,1)
# print trees.chooseBestFeatureToSplit(myDat)
# myTree = trees.createTree(myDat,labels)
# print myTree
import treePlotter
reload(treePlotter)
myTree = treePlotter.retrieveTree(0)
# treePlotter.createPlot(myTree)
# print labels
# print myTree
# print trees.classify(myTree,labels,[1,0])
# trees.storeTree(myTree,'classifierStorage.txt')
# print trees.grabTree('classifierStorage.txt')
fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels = ['age','prescript','astigmatic','tearRate']
lensesTree = trees.createTree(lenses,lensesLabels)
print lensesTree
treePlotter.createPlot(lensesTree)