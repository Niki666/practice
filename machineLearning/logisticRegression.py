#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
author ： fangqianqi
time : 2017-03-03-11

基于L1惩罚和L2惩罚的LR回归模型

C是用于调节目标函数和惩罚项之间关系的
C越小，惩罚力度越大，所得到的w的最优解越趋近于0，或者说参数向量越稀疏
C越大，惩罚力度越小，越能体现模型本身的特征。

本例子是利用逻辑回归做数字分类
每个样本都是一个8x8的图片，将这些样本分为两类：0-4为一类，5-9为一类

"""

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.preprocessing import StandardScaler

# 读取图片数据
# 这个数据集中有共有10种数字图片，数字分别是0-9
# 每种类别的数字大概有180张图片，总共的图片数目为1797张
# 每幅图片的尺寸为8x8，即64个像素点
# 像素的变化范围是0-16
#
# 也就是说，每个样本点有64个特征
# 即本例中LR模型的特征维度为64
digits = datasets.load_digits()

# 将前12张数字图片显示出来
plt.figure(1)
for i in range(12):
    imageplot = plt.subplot(3, 4, i+1)
    plt.imshow(digits.images[i], interpolation='nearest',
                   cmap='binary', vmax=16, vmin=0)
    imageplot.set_title("digit %d" % i)

# 读取数据X和目标y，并将数据X归一化
# 归一化的结果是均值为0，方差为1，也就是常用的z变换
#
# 对于机器学习中的很多方法，比如SVM，L1、L2正则化的线性模型等等
# 对于数据，都有一个基本假设，就是数据每个特征都是以0为中心
# 并且所有特征的数据变化都在同一个数量级
# 如果有一个特征的方差特别大，那么这个特征就有可能对机器学习的模型起决定性的作用
# 为了防止上面的现象，所以这里将数据做了归一化，或者叫做正则化
X, y = digits.data, digits.target
X = StandardScaler().fit_transform(X)

# 将数据集分成两类 0-4之间为一类，5-9之间为另一类
y = (y > 4).astype(np.int)


plt.figure(2)
for i, C in enumerate((100, 1, 0.01)):
    # 根据不同的C得到不同的LR模型
    clf_l1_LR = LogisticRegression(C=C, penalty='l1', tol=0.01)
    clf_l2_LR = LogisticRegression(C=C, penalty='l2', tol=0.01)
    clf_l1_LR.fit(X, y)
    clf_l2_LR.fit(X, y)

    # LR模型的参数向量
    coef_l1_LR = clf_l1_LR.coef_.ravel()
    coef_l2_LR = clf_l2_LR.coef_.ravel()

    # 计算L1和L2惩罚下，模型参数w的稀疏性
    sparsity_l1_LR = np.mean(coef_l1_LR == 0) * 100
    sparsity_l2_LR = np.mean(coef_l2_LR == 0) * 100

    print("C=%.2f" % C)
    print("L1惩罚项得到的参数的稀疏性: %.2f%%" % sparsity_l1_LR)
    print("L1惩罚项的模型性能: %.4f" % clf_l1_LR.score(X, y))
    print("L2惩罚项得到的参数的稀疏性: %.2f%%" % sparsity_l2_LR)
    print("L2惩罚项的模型性能: %.4f" % clf_l2_LR.score(X, y))

    l1_plot = plt.subplot(3, 2, 2 * i + 1)
    l2_plot = plt.subplot(3, 2, 2 * (i + 1))
    if i == 0:
        l1_plot.set_title("L1 penalty")
        l2_plot.set_title("L2 penalty")
        print coef_l1_LR

    l1_plot.imshow(np.abs(coef_l1_LR.reshape(8, 8)), interpolation='nearest',
                   cmap='binary', vmax=1, vmin=0)
    l2_plot.imshow(np.abs(coef_l2_LR.reshape(8, 8)), interpolation='nearest',
                   cmap='binary', vmax=1, vmin=0)
    plt.text(-8, 3, "C = %.2f" % C)

    l1_plot.set_xticks(())
    l1_plot.set_yticks(())
    l2_plot.set_xticks(())
    l2_plot.set_yticks(())

plt.show()