#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from collections import Counter
import MeCab
from matplotlib import pyplot as plt, font_manager as fm
#import matplotlib.pyplot as plt, matplotlib.font_manager as fm

# この file から source file への相対パスを取得
w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/neko.txt.mecab'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))

# Mecabの結果を扱いやすいデータ構造に変換
listed_text = []
listed_sentence = []
with open(w_s_rel) as source_f:
    for i, word in enumerate(source_f):
        # if i >= 5000: break
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

# データ抽出
values = list(zip(*sorted(word_counter.items(), key = lambda w: -w[1]))[1])

# グラフ描画
fp = fm.FontProperties(fname='/Library/Fonts/AppleGothic.ttf')
plt.plot(values, '.')
plt.grid(axis='y')
plt.title(u'39. Zipfの法則', fontproperties=fp)
plt.xlabel(u'出現頻度順位', fontproperties=fp)
plt.ylabel(u'出現頻度', fontproperties=fp)
plt.loglog()
plt.show()
