#!/bin/sh
g++ fourargs.cpp -o fourargs
python fourargs.py 1 2 3 4 5 6
python fourargs.py 1 2 3
fourargs 1 2 3 4 5 6
fourargs 1 2 3

# Copyright 2017 Zhonghao Guo gzh1994@bu.edu