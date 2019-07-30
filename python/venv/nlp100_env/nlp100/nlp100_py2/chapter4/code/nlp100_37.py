#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from collections import Counter
import MeCab
import matplotlib.pyplot as plt
import matplotlib as mpl

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

# 単語の出現頻度のcounterを作る(1)
word_counter = Counter()
for sentence in listed_text:
    for word in sentence:
        if re.match(r'\*\s*', word['base']):
            word_counter[word['surface']] += 1
            #word_counter.update([word['surface']])
        else:
            word_counter[word['base']] += 1
            #word_counter.update([word['base']])

# # 単語の出現頻度のcounterを作る(2) ちょっと違う
# word_counter = Counter([word['base'] for sentence in listed_text for word in sentence])

# 上位データ抽出
size = 10
# sorted_word_counter = sorted(word_counter.items(), key = lambda w: -w[1])
# labels = [tuple[0] for tuple in sorted_word_counter[:size]]
# values = [tuple[1] for tuple in sorted_word_counter[:size]]
#     # sorted(dict) の戻り値は tuple の list なので keys メソッドや values メソッドは使えないことに注意。
extracted_word_counter = word_counter.most_common(size)
labels = labels = [tuple[0] for tuple in extracted_word_counter]
values = [tuple[1] for tuple in extracted_word_counter]
    # Counter.most_common() の戻り値は tuple の list なので keys メソッドや values メソッドは使えないことに注意。

# グラフ描画
mpl.rcParams['font.family'] = u'AppleGothic'  # フォント設定
for i in range(10):
    print(labels[i] + str(values[i]))
plt.bar(labels, values)
plt.grid()
plt.show()
