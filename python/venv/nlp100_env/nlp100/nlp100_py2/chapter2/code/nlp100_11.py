#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

# t:this file, s:source file, o:output file, w:working directory
t_s_rel = '../data/hightemp.txt'
t_o_rel =  '../data/output11.txt'
w_t_rel = os.path.dirname(__file__)
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))
w_o_rel = os.path.normpath(os.path.join(w_t_rel, t_o_rel))

source_f = open(w_s_rel, 'r')
output_f = open(w_o_rel, 'w')
output_f.write(source_f.read().replace("\t", " "))
source_f.close
output_f.close


# Unix command
# expand -t 1 ./chapter2/data/hightemp.txt > ./chapter2/data/output11u_1.txt
# tr "\t" " " < ./chapter2/data/hightemp.txt > ./chapter2/data/output11u_2.txt
# sed -e 's/[[:space:]]/ /g' ./chapter2/data/hightemp.txt > ./chapter2/data/output11u_3.txt
# sed -e $'s/\t/ /g' ./chapter2/data/hightemp.txt > ./chapter2/data/output11u_3.txt
# sed -e 's/\t/ /g' ./chapter2/data/hightemp.txt > ./chapter2/data/output11u_3.txt はタブ認定されないので注意
