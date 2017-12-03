#include <iostream>
int main(int argumentcount, char** arguments)
{
if(argumentcount>4){
	for(int i=1;i<5;i++){
		std::fprintf(stdout,"%s\n",arguments[i]);
	}
	for(int j=5;j<argumentcount;j++){
		std::fprintf(stderr,"%s\n",arguments[j]);
	}
}
else{
	for(int k=1;k<argumentcount;k++){
		std::fprintf(stdout,"%s\n",arguments[k]);
	}
}
	return 0;
}

// Copyright 2017 Zhonghao Guo gzh1994@bu.edu
