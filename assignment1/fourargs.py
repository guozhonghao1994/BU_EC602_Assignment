# Copyright 2017 Zhonghao Guo gzh1994@bu.edu
import sys
if(len(sys.argv)>5):
 for i in range(1,5):sys.stdout.write(sys.argv[i]+'\n')

 for j in range(5,len(sys.argv)):sys.stderr.write(sys.argv[j]+'\n')


else:
 for k in range(1,len(sys.argv)):sys.stdout.write(sys.argv[k]+'\n')

 
