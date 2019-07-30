#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

class Morph:
    def __init__(self, surface, base, pos, pos1):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1
    def __str__(self):
        return '%s\t%s\t%s\t%s' % (self.surface, self.base, self.pos, self.pos1)

# get relative path from working directory
def rel_path(rel_path_from_this_file):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path_from_this_file))

# cabochaの解析結果を成型
listed_text = []
listed_sentence = []
with open(rel_path('../data/neko.txt.cabocha')) as source_f:
    for i, word in enumerate(source_f):
        if i >= 100: break
        if word == 'EOS\n':
            listed_text.append(listed_sentence)
            listed_sentence = []
        else:
            if word[:2] == '* ': continue
            #word = word.replace('\t', ',').split(',')
            word = re.split(r'[\t,]', word)
            listed_sentence.append(Morph(word[0], word[7], word[1], word[2]))

# 出力
for i, sentence in enumerate(listed_text, 1):
    if i == 3:
        for word in sentence:
            print(word)
        break
