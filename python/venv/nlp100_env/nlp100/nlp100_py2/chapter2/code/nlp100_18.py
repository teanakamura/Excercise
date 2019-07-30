#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# t:this file, s:source file, o:output file, w:working directory
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/hightemp.txt'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))

# with open(w_s_rel) as f:
#     lines = [l.split() for l in f]
# lines.sort(key = lambda l: l[2], reverse = True)
# for l in lines:
#     print('\t'.join(l))

with open(w_s_rel) as f:
    lines = f.readlines()
lines.sort(key=lambda l: float(l.split()[2]), reverse=True)
for l in lines:
    print(l.rstrip('\n'))


'''
Unix command
    sort -r -k 3 ./chapter2/data/hightemp.txt
'''
