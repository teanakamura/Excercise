#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import MeCab

w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/neko.txt.mecab'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))
print(w_s_rel)

listed_text = []
listed_sentence = []
with open(w_s_rel) as source_f:
    for i, word in enumerate(source_f):
        # if i >= 30: break
        if word == 'EOS\n':
            listed_text.append(listed_sentence)
            listed_sentence = []
        else:
            #word = word.replace('\t', ',').split(',')
            word = re.split(r'[\t,]', word)
            mapped_word = {
                'surface':word[0],
                'base':word[7],
                'pos':word[1],
                'pos1':word[2]
            }
            listed_sentence.append(mapped_word)
for sentence in listed_text:
    for word in sentence:
        print('%s\t%s\t%s\t%s' % (word['surface'], word['base'], word['pos'], word['pos1']))


'''
mecabの出力形式はデフォルトで表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
'''
