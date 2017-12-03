#Copyright 2017 Zhonghao Guo gzh1994@bu.edu
import numpy as np

x= np.array(input().split(' '))
h= np.array(input().split(' '))
y= np.empty(x.shape[0]+h.shape[0]-1)

for i in range(y.shape[0]):
 	y[i]=0

for j in range(x.shape[0]):
 	for k in range(h.shape[0]):
 		y[j+k]+=float(x[j])*float(h[k])

for element in range(y.shape[0]):
	print((y[element]),end=" ")
