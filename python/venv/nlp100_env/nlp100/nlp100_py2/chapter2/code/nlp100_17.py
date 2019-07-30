#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# t:this file, s:source file, o:output file, w:working directory
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/hightemp.txt'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))
with open(w_s_rel) as f:
    pre_set = set()
    for line in f:
        pre_set.add(line.split()[0].decode('utf-8'))
for w in pre_set:
    print(w)        #ASCII文字列でないので print(pre_set)としてもうまく出力できない


'''
Unix command
    cut -f 1 ./chapter2/data/hightemp.txt | sort | uniq
'''
