#coding:utf-8
import matplotlib.pyplot as plt
import numpy as np
var = np.random.randn(5300)
plt.hist(var,530)
plt.title(r'sdsdsdsd')
plt.show()

r = [1.5,2.0,3.5,4.0,5.5,6.0]
a = [7.06858,12.56637,38.48447,50.26544,95.03309,113.09724]
plt.plot(r,a)
plt.xlabel('Radius')
plt.ylabel('Area')
plt.title('Area of Circle')
plt.show()

var = np.arange(0.,100,0.2)
cos_var = np.cos(var)
sin_var = np.sin(var)
plt.plot(var,cos_var,'b-*',label='cosine')
plt.plot(var,sin_var,'r-.',label='sine')
plt.legend(loc='upper left')
plt.xlabel('xaxis')
plt.ylabel('yaxis')
plt.ylim(-2,2)
plt.show()

