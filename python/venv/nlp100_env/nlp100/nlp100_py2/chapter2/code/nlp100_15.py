#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def tail(path, num):
    with open(path) as f:
        lines = f.readlines()
        for line in lines[-num:]:
            print(line.rstrip())

# t:this file, s:source file, o:output file, w:working directory
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/hightemp.txt'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))

print("how manu lines do you want?")
num = int(raw_input())
tail(w_s_rel, num)


'''
Unix command
    read N
    tail -n $N ./chapter2/data/hightemp.txt
'''
