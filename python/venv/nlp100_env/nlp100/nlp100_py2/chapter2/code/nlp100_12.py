#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

# t:this file, s:source file, o:output file, w:working directory, od:ourput directory
t_s_rel = '../data/hightemp.txt'
t_od_rel =  '../data/'
w_t_rel = os.path.dirname(__file__)
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))
w_od_rel = os.path.normpath(os.path.join(w_t_rel, t_od_rel))

# col_n = 2
# f = [''] * col_n
# with open(w_s_rel) as source_file:
#         for i, j in enumerate(range(col_n), 1):
#             w_o_rel = os.path.join(w_od_rel, "output12%d.txt" % i)
#             f[j] = open(w_o_rel, 'w')
#         for line in source_file:
#             for j in range(col_n):
#                 f[j].write(line.split()[j] + "\n")
#         # line = source_file.readline()
#         # while line:
#         #     for j in range(col_n):
#         #         f[j].write(line.split()[j] + "\n")
#         #     line = source_file.readline()
#         for j in range(col_n):
#             f[j].close

def col_file(num):
    with open(w_s_rel) as source_file:
        w_o_rel = os.path.join(w_od_rel, "output12_col%d.txt" % num)
        with open(w_o_rel, 'w') as f:
            for line in source_file:
                f.write(line.split()[num-1] + "\n")
col_file(1)
col_file(2)



# Unix command
# cut -f 1 ./chapter2/data/hightemp.txt > ./chapter2/data/output12u_col1.txt
# cut -f 2 ./chapter2/data/hightemp.txt > ./chapter2/data/output12u_col2.txt
