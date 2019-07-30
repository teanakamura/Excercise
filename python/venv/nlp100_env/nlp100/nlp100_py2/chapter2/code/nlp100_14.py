#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

def head(path, num):
    with open(path) as f:
        for i in range(num):
            sys.stdout.write(f.readline())
            #print(f.readline().rstrip("\n"))

# def head(path, num):
#     with open(path) as f:
#         for i, line in enumerate(f):
#             if i >= num:
#                 break
#             print(line.rstrip())

# t:this file, s:source file, o:output file, w:working directory
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/hightemp.txt'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))

print("how manu lines do you want?")
num = int(raw_input())
head(w_s_rel, num)


'''
Unix command
    read N
    head -n $N ./chapter2/data/hightemp.txt
'''
