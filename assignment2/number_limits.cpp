// Copyright 2017 Zhonghao Guo gzh1994@bu.edu
#include <iostream>
#include <cfloat>
#include <cstdint>
#include <cmath>
using namespace std;

int main(){
    double Rs,Rm,Ri;
	Rs=1/(pow(2,-14));//correct
	Rm=(double)65504/32767;//correct
	Ri=(int)15;
	cout<<"16 : Ri= "<<Ri<<" Rm= "<<Rm<<" Rs= "<<Rs<<endl;

	Rs=1/FLT_MIN;//correct
	Rm=(double)FLT_MAX/2147483647;//correct
	Ri=(int)2147483647/pow(2,24)-1;
	cout<<"32 : Ri= "<<Ri<<" Rm= "<<Rm<<" Rs= "<<Rs<<endl;

	Rs=1/DBL_MIN;//correct
	Rm=(double)DBL_MAX/9223372036854775807;//correct
	Ri=(double)9223372036854775807/pow(2,53)-1;
	cout<<"64 : Ri= "<<Ri<<" Rm= "<<Rm<<" Rs= "<<Rs<<endl;
	system("pause");
	return 0;	
}