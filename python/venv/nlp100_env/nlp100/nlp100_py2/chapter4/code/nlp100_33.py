#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import MeCab

# この file から source file への相対パスを取得
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/neko.txt.mecab'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))

# Mecabの結果を扱いやすいデータ構造に変換
listed_text = []
listed_sentence = []
with open(w_s_rel) as source_f:
    for i, word in enumerate(source_f):
        if i >= 500: break
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

# さ変接続の名詞の原形のsetを作る
nouns_list = [word['base']
    for sentence in listed_text
    for word in sentence
    if word['pos'] == '名詞' and word['pos1'] == 'サ変接続']
nouns_set = set(nouns_list)

# 出力
for noun in sorted(nouns_set, key = nouns_list.index):
    print(noun + '\t'),
print('')
