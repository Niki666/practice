#coding:utf-8
#计算函数最小值
import numpy as np
from scipy.optimize import minimize
#定义函数
def rosenbroken(x):
    return sum(100.0*(x[1:]-x[-1]**2.0)**2.0+(1-x[-1])**2.0)
x0 = np.array([1,0.7,0.8,2.9,1.1])
res = minimize(rosenbroken,x0,method='nelder-mead',options={'xtol':1e-8,'disp':True})
print(res.x)

#图像处理
# from scipy import misc
# l = misc.lena()
# misc.imsave('lena.png',l)
# import matplotlib.pyplot as plt
# plt.gray()
# plt.imshow()
# plt.show()

