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
        if i >= 5000: break
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

# 名詞の連接の原形のsetを作る(1)
noun_phrases_list = []
noun_phrase = []
for sentence in listed_text:
    for word in sentence:
        if word['pos'] == '名詞':
            noun_phrase.append(word['surface'])
        else:
            if len(noun_phrase) > 1: noun_phrases_list.append(''.join(noun_phrase))
            noun_phrase = []
noun_phrases_set = set(noun_phrases_list)

# 出力
for noun in sorted(noun_phrases_set, key = noun_phrases_list.index):
    print(noun + '\t'),
print('')
