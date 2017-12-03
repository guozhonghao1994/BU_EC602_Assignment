//Copyright 2017 Zhonghao Guo gzh1994@bu.edu

#include <iostream>
#include <cstdint>
#include <cfloat>
#include <cmath>
using namespace std;

int main(){
  double estimate,lower,upper;
  double earth_mass = 15*(1e11);//kilogram
  double O_rmass = 2.657*(1e-26);//O_mass
  double Si_rmass = 4.66*(1e-26);
  double Al_rmass =4.48*(1e-26);
  double Fe_rmass =9.288*(1e-26);
  double O = earth_mass*0.466/O_rmass*8;
  double Si =earth_mass*0.277/Si_rmass*14;
  double Al =earth_mass*0.081/Al_rmass*13;
  double Fe =earth_mass*0.050/Fe_rmass*26;
  estimate=O+Si+Al+Fe;
  lower=0.95*estimate;
  upper=estimate*1.05;

  cout<<estimate<<endl;
  cout<<lower<<endl;
  cout<<upper<<endl;
  system("pause");
  return 0;
}