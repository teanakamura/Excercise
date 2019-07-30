#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def file_merge(path1, path2, merge_path):
    with open(path1, 'r') as f1, \
          open(path2, 'r') as f2,\
          open(merge_path, 'w') as mf:
        for l1, l2 in zip(f1, f2):
            mf.write(l1.rstrip("\n") + "\t" + l2)

# t:this file, s:source file, o:output file, w:working directory
w_t_rel = os.path.dirname(__file__)
t_s1_rel = '../data/output12_col1.txt'
t_s2_rel = '../data/output12_col2.txt'
t_o_rel =  '../data/output13.txt'
w_s1_rel = os.path.normpath(os.path.join(w_t_rel, t_s1_rel))
w_s2_rel = os.path.normpath(os.path.join(w_t_rel, t_s2_rel))
w_o_rel = os.path.normpath(os.path.join(w_t_rel, t_o_rel))

file_merge(w_s1_rel, w_s2_rel, w_o_rel)

# unix command
# paste ./chapter2/data/output12_col1.txt ./chapter2/data/output12_col2.txt > ./chapter2/data/output13u.txt
# diff --report-identical-files ./chapter2/data/output13.txt ./chapter2/data/output13u.txt
