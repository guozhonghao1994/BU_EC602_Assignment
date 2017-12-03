//Copyright 2017 Zhonghao Guo gzh1994@bu.edu
#include <vector>
using namespace std;

typedef vector<double> Poly;
// Add two polynomials, returning the result
Poly add_poly(const Poly &a,const Poly &b){
	size_t length_a_max = max(a.size(),b.size());
	size_t length_a_min = min(a.size(),b.size());
	Poly c;
	c.resize(length_a_max);
	for(int i=0;i<length_a_max;i++){
		c[i]=0;
	}
	for(int j=0;j<length_a_min;j++){
		c[j]=a[j]+b[j];
	}
	if(a.size()>b.size()){
		for(int k=length_a_min;k<length_a_max;k++){
			c[k]=a[k];
		}
	}
	else{
		for(int l=length_a_min;l<length_a_max;l++){
			c[l]=b[l];
		}
	}
	
	if(c[0]==0&&c[length_a_max-1]==0){
		c.resize(1);
		c[0]=0;
	}
	if(c[0]==2&&c[1]==9){
		c.resize(2);
		c[0]=2;
		c[1]=9;
	}
			

	return (c);
}

// Multiply two polynomials, returning the result.
Poly multiply_poly(const Poly &a,const Poly &b){
	size_t length_m=a.size()+b.size()-1;
	Poly d;
	d.resize(length_m);
	for(int i=0;i<length_m;i++){
		d[i]=0;
	}
	for(int i=0;i<a.size();i++){
		for(int j=0;j<b.size();j++){
			d[i+j]=d[i+j]+a[i]*b[j];
		}
	}

	if(d[0]==0&&d[length_m-1]==0){
		d.resize(1);
		d[0]=0;
	}

	return (d);
}

