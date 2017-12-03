#Copyright 2017 Zhonghao Guo gzh1994@bu.edu

from numpy import zeros, exp, array, pi


def DFT(x):	
	try:
		if type(x) is dict:
			raise Exception()		
		
		N = len(x)	
		X = zeros(N, dtype="complex")	
		for k in range(0,N):
			for n,x_n in enumerate(x):								
				X[k]+=x_n*exp(-2j*pi*n*k/N)
		return X
	except:
		raise ValueError("Invalid input encountered")		

def main():
	x = bytearray([1,2,3,4])
	X = DFT(x)
	print("x: ", x)
	print(x[0])
	print("X1: ", X)



if __name__=="__main__":
	main()
