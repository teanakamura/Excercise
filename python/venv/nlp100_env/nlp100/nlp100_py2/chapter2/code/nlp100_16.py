#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def split(path, num):
    with open(path) as source_file:
        lines = source_file.readlines()
    file_size = -(-len(lines) // num)   #切り上げの計算
    print(file_size)
    # for n in range(1, num+1):
    #     with open(os.path.join(os.path.dirname(path), "output16_split%d.txt" % n), 'w') as f:
    #         for line in lines[file_size*(n-1):file_size*n]:
    #             f.write(line)  #printは自動で改行が挿入されるがwriteは挿入されない
    for n, offset in enumerate(range(0, len(lines), file_size), 1):
        with open(os.path.join(os.path.dirname(path), "output16_split%d.txt" % n), 'w') as f:
            for line in lines[offset : offset + file_size]:
                f.write(line)  #printは自動で改行が挿入されるがwriteは挿入されない

# t:this file, s:source file, o:output file, w:working directory
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/hightemp.txt'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))

print("how manu lines do you want?")
num = int(raw_input())
split(w_s_rel, num)


'''
Unix command
    read N
    len=$(cat ./chapter2/data/hightemp.txt | wc -l)
    # len=$(wc -l ./chapter2/data/hightemp.txt | awk '{print $1}')
    file_size=$((-(-$len/$N)))
    split -l $file_size ./chapter2/data/hightemp.txt ./chapter2/data/output16u_split  #free_BSD
    # split -l $file_size -d --additional-suffix=.txt ./data/hightemp.txt ./data/hightemp_split_u  #Linux
'''
