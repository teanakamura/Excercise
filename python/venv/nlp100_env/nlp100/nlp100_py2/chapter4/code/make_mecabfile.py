#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import MeCab

w_t_rel = os.path.dirname(__file__)
t_s_rel = '../data/neko.txt'
w_s_rel = os.path.normpath(os.path.join(w_t_rel, t_s_rel))
print(w_s_rel)

with open(w_s_rel) as source_f:
    with open(os.path.join(os.path.dirname(w_s_rel), 'neko.txt.mecab'), 'w') as output_f:
        mecab_tagger = MeCab.Tagger('')
        # parsed = mecab_tagger.parse(source_f.read())  # この手法だと文の境界の判定ができない。
        # output_f.write(parsed)
        for line in source_f:
            parsed = mecab_tagger.parse(line)
            output_f.write(parsed)
