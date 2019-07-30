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

# # 動詞の原形のsetを作る(1)
# verbs_set = set()   # set()は空のsetを生成し、{}は空のdictを生成する。
# verbs_list = []
# for sentence in listed_text:
#     for word in sentence:
#         if word['pos'] == '動詞':
#             verbs_set.add(word['base'])
#             verbs_list.append(word['base'])  # 出てきた順に出力できるように出現順のlistを作成。

# 動詞の原形のsetを作る(2) 内包表記を使うと二行でできる。
verbs_list = [word['base'] for sentence in listed_text for word in sentence if word['pos'] == '動詞']
# verbs_set = {word['base'] for sentence in listed_text for word in sentence if word['pos'] == '動詞'}
    # 先の for が外側のループになるので注意。
verbs_set = set(verbs_list)

# 出力
for verb in sorted(verbs_set, key = verbs_list.index):
    print(verb + '\t'),
print('')
