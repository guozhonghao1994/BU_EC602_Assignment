# Copyright 2017 Zhonghao Guo gzh1994@bu.edu
Table = "{:<6} {:<22} {:<22} {:<22}"
print(Table.format('Bytes','Largest Unsigned Int','Minimum Signed Int','Maximum Signed Int'))
for i in range(1,9):
	Largest_Unsigned_Int= 2**(8*i)-1
	Minimum_Signed_Int= -2**(8*i-1)
	Maximum_Signed_Int= 2**(8*i-1)-1
	print(Table.format(i,Largest_Unsigned_Int,Minimum_Signed_Int,Maximum_Signed_Int))
