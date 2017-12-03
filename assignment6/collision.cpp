//Copyright 2017 Zhonghao Guo gzh1994@bu.edu
//Copyright 2017 Yujia Wang yujia8@bu.edu
//Copyright 2017 Yuchen Wang wangyc95@bu.edu 

#include <vector>
#include <string.h>
#include <iostream>
#include <cstdlib>
#include <algorithm>
#include <sstream>
#include <iterator>
#include <cfloat>
#include <cmath>
#include <iomanip>

using namespace std;


int main(int argc, char *argv[])
{
	double delta=0.000001;
//get input time 
	double time[argc-1];
	for (int i=1;i<argc;i++){
		for(int j=0;j<strlen(argv[i]);j++){
			if(j==0 && ((argv[i][j]==43)||(argv[i][j]==43)))
				continue;
			if ((argv[i][j]>57)||(argv[i][j]<46))			
				return 2;
		}
		time[i-1]=atof(argv[i]);
	}
	sort(time,time+argc-1);
	
//get input balls
	string line;  
	vector<string> temp;
	vector<vector<double> > balls;
	vector<string> ID;

	while(getline(cin,line))  
		temp.push_back(line);
	
	balls.resize(temp.size());
	int num = temp.size();

	for (int i=0;i<temp.size();i++){
		istringstream iss(temp[i]);
		vector<string> entries{istream_iterator<string>{iss},istream_iterator<string>{}};
		
		if(entries.size()!=5)
			return 1;

		for (int j=0;j<entries.size();j++){
			if (j==0)
				ID.push_back(entries[j]);
			
			else{
				for(int m=0;m<entries[j].size();m++)
				{
					if(m==0 && ((entries[j][m]==45)||(entries[j][m]==43)))
						continue;
					if (((entries[j][m]>57)||(entries[j][m]<46)))			
						return 1;
				}		
				balls[i].push_back(stod(entries[j]));	
			}
		}
	}
		
//calculate
	double distance;
	double dtime=0;
	double dt, t1, t2;
	for(int i=0;i<argc-1;i++)
	{
		while(dtime<time[i])
		{
	    		dt=time[i]-dtime;
			for(int a=0;a<balls.size();a++)
			{
				for(int b=a+1;b<balls.size();b++)
				{
					double p=pow((balls[a][2]-balls[b][2]), 2) + pow((balls[a][3]-balls[b][3]), 2);
					double q=2*((balls[a][0]-balls[b][0])*(balls[a][2]-balls[b][2])+(balls[a][1]-balls[b][1])*(balls[a][3]-balls[b][3]));
					double r=pow((balls[a][0]-balls[b][0]), 2) + pow((balls[a][1]-balls[b][1]), 2) -100;
					double check = pow(q, 2) - 4*p*r;
					if(check > 0)
					{
						t1=(-sqrt(pow(q, 2)-4*p*r)-q)/(2*p);
						t2=(sqrt((pow(q, 2)-4*p*r))-q)/(2*p);
						if(t1>0 && t2>t1)
							dt=min(dt,t1);
					}
				}
			}

			for(int l=0;l<balls.size();l++)
    			{
    				balls[l][0]=(balls[l][0]+dt*balls[l][2]);
				balls[l][1]=(balls[l][1]+dt*balls[l][3]);
    			}
			for(int a=0;a<balls.size();a++)
    			{
				for(int b=a+1;b<balls.size();b++)
				{
					double x = (balls[a][0]-balls[b][0]);
					double y = (balls[a][1]-balls[b][1]);
					distance = (sqrt((pow(x,2)+pow(y,2))));
					if(distance<=10)
					{
						double inn=((balls[a][0]-balls[b][0])*(balls[a][2]-balls[b][2])+(balls[a][1]-balls[b][1])*(balls[a][3]-balls[b][3]));
						balls[a][2]=(balls[a][2]-(inn*(balls[a][0]-balls[b][0]))/100);
						balls[a][3]=(balls[a][3]-(inn*(balls[a][1]-balls[b][1]))/100);
						balls[b][2]=(balls[b][2]-(inn*(balls[b][0]-balls[a][0]))/100);
						balls[b][3]=(balls[b][3]-(inn*(balls[b][1]-balls[a][1]))/100);
					}

				}
			}
			dtime=dtime+dt;
    	}

    	cout << time[i] << endl;

    	for(int k=0;k<balls.size();k++)
    	{
    		cout << ID[k] << " ";
			for(int h=0;h<4;h++)
			{
				cout << setprecision(9) << balls[k][h] << " ";
				if(h == 3)
					cout << endl;
			}
    	}
    }
	return 0;
}


