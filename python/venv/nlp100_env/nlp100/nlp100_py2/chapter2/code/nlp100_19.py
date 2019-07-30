#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
破壊的メソッドは返り値がないことに注意。今回appendやsortは破壊的メソッド
'''

import collections
import os

# t:this file, s:source file, o:output file, w:working directory
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/hightemp.txt'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))

with open(w_s_rel) as f:
    lines = [l.split() for l in f]
col_dict = collections.Counter([l[0] for l in lines])
col_of_lines = [col_dict[l[0]] for l in lines]
lines = [line + [num] for line, num in zip(lines, col_of_lines)]
#[line.append(num) for line, num in zip(lines, col_of_lines)]  #返り値ないので代入はできない
#lines_with_col = dict(col_of_lines, col_dict)) 辞書にすると重複したkeyを作成できないのでこれはOUT
lines.sort(key = lambda l: l[0])
lines.sort(key = lambda l: l[-1], reverse = True)  #返り値ないので連続して使用できない。
for l in lines:
    print('\t'.join(l[:-1]))

#col_dictのみを使用するこっちだけで十分だったかも
for pre, num in sorted(col_dict.items(), key = lambda l: l[1],reverse = True):
        # dict型にsorted関数を適用するとtapleのlistが返る。
        # sorted関数でdict型のiterationが呼びだされるが、この際 .keys / .values / .items のいずれかを使ってループの対象を指定する必要がある。 
    print(str(num) + "\t" + pre)



'''
Unix command
    cut -f1 ./chapter2/data/hightemp.txt | sort | uniq -c | sort -nrk1  　#ちょっと出力違う
'''
