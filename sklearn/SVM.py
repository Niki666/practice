#coding:utf-8
from sklearn import svm
X = [[0,0],[1,1]]
y = [0,1]
clf = svm.SVC()
print clf.fit(X,y)
print clf.predict([[2,2]])
print clf.support_vectors_
print clf.support_
print clf.n_support_

#多类别分类
X = [[0],[1],[2],[3]]
Y = [0,1,2,3]
clf = svm.SVC(decision_function_shape='ovo')
print clf.fit(X,Y)
dec = clf.decision_function([[1]])
print dec.shape[1]  #󰀃4󰀃classes:󰀃4*3/2󰀃=󰀃6
clf.decision_function_shape = 'ovr'
dec = clf.decision_function([[1]])
print dec.shape[1]  #󰀃4󰀃classes

#󰀃LinearSVC󰀃实现了“一对多”分类法，因此会训练n_class个模型。
# 如果只有两个类别，那么只会得到一个模型：
lin_clf = svm.SVC()
print lin_clf.fit(X,Y)
dec = lin_clf.decision_function([[1]])
print dec.shape[1]


#回归
from sklearn import svm
