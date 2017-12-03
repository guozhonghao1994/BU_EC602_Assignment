// Copyright 2017 Zhonghao Guo gzh1994@bu.edu
#include <iostream>
#include <ctime>
#include <cmath>
#include <cstdint>
using namespace std;

int main(){
	clock_t start,end;
	start=clock();
	uint16_t b=1;
	while(b>0){
		b++;
	}
	end=clock();
	double time_16=(double)(end-start)*(1e6);
	double time_8=time_16*((pow(2,8)/pow(2,16)))*(1e3);
	double time_32=time_16*((pow(2,32)/pow(2,16)))*(1e-6);
	double time_64=time_16*((pow(2,64)/pow(2,16)))*(1e-6)/3600/24/365;


	cout<<"estimated int8 time (nanoseconds): "<<time_8<<endl;
	cout<<"measured int16 time (microseconds): "<<time_16<<endl;
	cout<<"estimated int32 time (seconds): "<<time_32<<endl;
	cout<<"estimated int64 time (years): "<<time_64<<endl;
	return 0;
}
