#coding:utf-8
from sklearn import linear_model
#最小二乘法
clf = linear_model.LinearRegression()
clf.fit([[0,0],[1,1],[2,2]],[0,1,2]) #X is list of three.y is last list
#print clf.coef_

#岭回归(ridge regression)
from sklearn import linear_model
clf = linear_model.Ridge(alpha=0.5)
clf.fit([[0,0],[0,0],[1,1]],[0,.1,1])
print clf.coef_   # 打印参数
print clf.intercept_   # 打印截距项

#使用广义交叉验证设置正则化参数
clf = linear_model.RidgeCV(alphas=[0.1,1.0,10.0])
clf.fit([[0,0],[0,0],[1,1]],[0,.1,1])
print clf.alpha_

#Lasso󰀃是一种预测稀疏系数的线性模型
clf = linear_model.Lasso(alpha=0.1)
clf.fit([[0,0],[1,1]],[0,1])
print clf.predict([1,1])

#󰀃LassoLars󰀃是一种使用LARS算法实现的lasso模型。和基于坐标下降的实现不同，
# 该模型产生确切解，是其系数范数函数的逐步线性
clf = linear_model.LassoLars(alpha = .1)
clf.fit([[0,0],[1,1]],[0,1])
print clf.coef_

#贝叶斯岭回归
X = [[0.,0.],[1.,1.],[2.,2.],[3.,3.]]
Y = [0.,1.,2.,3.]
clf = linear_model.BayesianRidge()
clf.fit(X,Y)
print clf.predict([[1,0.]])
print clf.coef_
#由于贝叶斯框架的原因，该方法得到的权重与通过普通最小二乘得到的参数略有差别。
# 不过贝叶斯岭回归对ill-posed问题有更强的鲁棒性。

#多项式回归：使用基本函数扩展线性模型
#图像创建之前使用了󰀃PolynomialFeatures󰀃进行预处理
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
X = np.arange(6).reshape(3,2)
print X
poly = PolynomialFeatures(degree = 2)
print poly.fit_transform(X)

#简单多项式回归的对象可以如下创建
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import numpy as np
model = Pipeline([('poly',PolynomialFeatures(degree=3)),
                  ('linear',LinearRegression(fit_intercept=False))])
x = np.arange(5)
y = 3 - 2 * x + x ** 2 - x ** 3
model = model.fit(x[:, np.newaxis],y)
print model.named_steps['linear'].coef_

# 用线性分类器解决异或问题
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = X[:,0]^X[:,1]  #^ 按位异或.  按位异或运算 按位异或运算符“^”是双目运算符。其功能是参与运算的两数各对应的二进位相异或，
# 当两对应的二进位相异时，结果为1。如： 00001001^00000101 00001100
X = PolynomialFeatures(interaction_only=True).fit_transform(X)
print X
clf = Perceptron(fit_intercept=False,n_iter=10,shuffle = False).fit(X,y)
print clf.score(X,y) #计算准确率