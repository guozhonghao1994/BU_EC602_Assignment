#!/usr/bin/env python
# Copyright 2017 Weixuan Jiang jwx0728@bu.edu
# Copyright 2017 Tong Ye tongyewh@bu.edu
# Copyright 2017 Shanshan Zhao zhaoss@bu.edu
import sys

def _input():
	#a1 = []
	b1 = []

	if len(sys.argv) == 1:
		exit(2)

	try:
		for i in range(1,len(sys.argv)):
			k = float(sys.argv[i])
			if k < 0 :
				exit(2)
	except:
		exit(2)


	for line in sys.stdin:
		b1.append(line.split())
		#print("!!!!!!!*",b1)
		for h in range(len(b1)) :
			if len(b1[h]) != 5 :
				exit(1)
			#print("!!!!!!!*",b1)
			try :
				b1[h][1] = float(b1[h][1])
				b1[h][2] = float(b1[h][2])
				b1[h][3] = float(b1[h][3])
				b1[h][4] = float(b1[h][4])
			except Exception:
				exit(1)


		#a1.append(b1)
		#print("!!!!!!!",b1)
		#pass
	return b1

def IsCollide(list1 = [],list2=[],set_time = 0):
	"if return time=0  means no collision"
	time1 = -999
	time2 = -999
	x1=list1[1]
	x2=list2[1]

	x = x2-x1
	#print("!!!x",x)
	y1=list1[2]
	y2=list2[2]

	y = y2-y1
	#print("!!!y",y)
	vx1=list1[3]
	vx2=list2[3]

	vx = vx2-vx1
	#print("!!!vx",vx)
	vy1=list1[4]
	vy2=list2[4]

	vy = vy2-vy1
	#print("!!!vy",vy)
	time = 0

	a = vx**2 + vy**2

	if a == 0 :
		return set_time+1
	

	b = 2.0*(vx*x+vy*y)

	c = x**2 + y**2 -100.0
	#print("******",a,"  ",b,"  ",c)
	#print("@@@@@@@",b**2 - 4.0*a*c)

	if b**2 - 4.0*a*c >= 0:
		time1 = ((0.0-b) + (b**2 - 4.0*a*c)**0.5) / (2.0 * a)
		time2 = ((0.0-b) - (b**2 - 4.0*a*c)**0.5) / (2.0 * a)
		if time1 > time2 and time2>=0:
			time = time2
		else :
			if time1 > 0:
				time = time1
			else :
				time = set_time+1
	else :
		time = set_time+1

	#print("^^^^^",time1,"   ",time2)
	if time < 0.00000000000001 and time != 0:
		time = set_time+1#time = 0

	return time
		
def relocat_withoutcolli(list1 = [],t = 0.0):
	
	for i in range(len(list1)):
		list1[i][1] += list1[i][3] * t #reloc x
		list1[i][2] += list1[i][4] * t #reloc y

	return list1

def relocation(list1 = [],list2 = []):
	i = 0
	p = len(list2) / 3
	f = []
	t = list2[0]
	#print("!!!!!!!!",list1[0][2])
	for l in range(len(list1)):
		#print("!!!!!!!!",list1[i][1])
		list1[l][1] = list1[l][1] + list1[l][3] * t #reloc x
		#print("!!!!!!!!",list1[i][1])
		list1[l][2] += list1[l][4] * t #reloc y

	while p != 0:
		#t = list2[i]#collision time
		#print("$$$$$$$$$$$",t)
		a = list2[i+1]# first ball
		b = list2[i+2]# second ball
		f.append(a)
		f.append(b)
		i=i+3
		p = p-1
		#print("$$$$$$$$$$$",t,"  ",a,"  ",b)
	change = []
	after = []
	i = 0
	while i != len(f) :
		change.append(list1[f[i]])
		change.append(list1[f[i+1]])
		after = collision(change)
		list1[f[i]][3] = after[0][3]
		list1[f[i]][4] = after[0][4]
		list1[f[i+1]][3] = after[1][3]
		list1[f[i+1]][4] = after[1][4]
		i = i+2
		change = []

	return list1

def collision(list1=[]):
	x1=list1[0][1]
	y1=list1[0][2]
	xv1=list1[0][3]
	yv1=list1[0][4]

	x2=list1[1][1]
	y2=list1[1][2]
	xv2=list1[1][3]
	yv2=list1[1][4]

	_xv = xv1-xv2

	xv_ = xv2-xv1
	
	_yv = yv1-yv2

	yv_ = yv2-yv1

	_x = x1-x2

	x_ = x2-x1

	_y = y1-y2
	y_ = y2-y1

	neiji1 = _xv * _x + _yv * _y
	neiji2 = xv_ * x_ + yv_ * y_


	list1[0][3] = xv1 - (neiji1/100.0) * _x
	list1[0][4] = yv1 - (neiji1/100.0) * _y

	list1[1][3] = xv2 - (neiji2/100.0) * x_
	list1[1][4] = yv2 - (neiji2/100.0) * y_

	#print("&&&&&",list1)
	return list1

def result(list1 = []):
		for i in list1 :
			for j in i :
				print(j,end=" ")
			print(" ")


def main():
	t_list = []
	index = []
	temp = []
	a = []
	a_copy = []
	real_time = 0
	time_count = 0
	left_time = 0

	a_copy = _input()
	
	#print("zong shuzu: ",a)
	n = len(sys.argv) -1
	m = 1
	#!!
	while n :
		a = []
		aa = []
		t_list = []
		index = []
		temp = []
		real_time = 0
		time_count = 0
		left_time = 0
		settime = float(sys.argv[m])
		#print("+++++++",a_copy)
		#a = a_copy.copy()
		#print("&&&&&&&&",a_copy)
		for i in range(len(a_copy)) :
			aa = []
			for j in range(len(a_copy[i])) :
				aa.append(a_copy[i][j])
			a.append(aa)
		#print("****",a)
		
		while 1 :
			t_list = []
			temp = []
			for i in range(len(a)):
				for j in range(i+1,len(a)):
					#print("for loop  a: ",a)
					index.append(IsCollide(a[i],a[j],settime))
					index.append(i)
					index.append(j)
					t_list.append(index)
					index = []
			#print("!!!",t_list)
			if len(t_list) > 0 :
				real_time = t_list[0][0]
				for i in t_list:
					if i[0] < real_time :
						real_time = i[0]
				#print("***********",real_time)

				for i in t_list:
					if i[0] == real_time:
						for e in i:
							temp.append(e)
				#print("$$$$$$$$$$$ ",temp)
			else :
				real_time = settime+1
		#if real_time == 0 :
			#print("%%%%%%%%%%%",time_count)
			if real_time > settime :
				left_time = settime - time_count
				#print("%****&%",time_count)
				a = relocat_withoutcolli(a,left_time)
				#print("run realtime=0",a)
				break
			elif real_time == settime :
				left_time = settime - time_count
				a = relocation(a,temp)
				#print("real_time == settime ",a)
				break
			elif real_time == 0 :
				left_time = settime - time_count
				a = relocation(a,temp)
				#a = relocat_withoutcolli(a,left_time)
				#print("real_time == 0 ",a)
				#break
			else :
				if real_time + time_count > settime :
					left_time =  settime - time_count
					#print("^^^^^^^",left_time)
					a = relocat_withoutcolli(a,left_time)
					#print("relocat_withoutcolli ",a)
					break
				else :
					time_count += real_time
					a = relocation(a,temp)
					#print("continue ",a)
					#print("^^^^^^^",temp)
				#print("######",time_count)
				#if time_count <= float(sys.argv[m]) :
				#	a = relocation(a,temp)
				#	print("^^^^^^^",temp)
					#print("run relocation",a)
				#else :
				#	left_time =  float(sys.argv[m]) - time_count
				#	print("^^^^^^^",left_time)
				#	a = relocat_withoutcolli(a,left_time)
					#print("run withoutcollision",a)
				#	break
		
		print(sys.argv[m])
		result(a)
		n = n-1
		m = m+1
	#print("final",a)

	


if __name__ == '__main__':
    main()
