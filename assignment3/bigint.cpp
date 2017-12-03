//Copyright 2017 Zhonghao Guo gzh1994@bu.edu
#include <vector>
#include <string>
using namespace std;

typedef string BigInt;
BigInt multiply_int(const BigInt &a,const BigInt &b){
	BigInt res="";
	int m=a.size(), n=b.size();
	vector<long long>tmp(m+n-1);

	for(int i=0;i<m;i++){
		int c=a[i]-'0';
		for(int j=0;j<n;j++){
			int d=b[j]-'0';
			tmp[i+j]=tmp[i+j]+c*d;
		}
	}

	int carry=0;
	for(int i=tmp.size()-1;i>=0;i--){
		int t=tmp[i]+carry;
		tmp[i]=t%10;
		carry=t/10;
	}

	while(carry!=0){
		int t=carry%10;
		carry /=10;
		tmp.insert(tmp.begin(),t);
	}

	for(auto a:tmp){
		res=res + to_string(a);
	}
	if(res.size()>0 && res[0]=='0')return "0";
	return res;


}
