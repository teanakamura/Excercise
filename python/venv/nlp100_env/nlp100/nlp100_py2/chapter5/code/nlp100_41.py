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


class Chunk:
    def __init__(self, morphs = None, dst = None, src = None):
            # []などのmutableなオブジェクトをデフォルト値とする際は注意。Noneなどを使えば気にしなくて良い。
        self.morphs = [] if morphs is None else morphs
        self.dst = '' if dst is None else dst
        self.src = [] if src is None else src
    def __str__(self):
        return ('surface:%s\tdst:%d\tsrc:%s\n' \
                % (''.join([m.surface for m in self.morphs]), self.dst, ', '.join(map(str, self.src)))).rstrip('\n')


# get relative path from working directory
def rel_path(rel_path_from_this_file):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path_from_this_file))


# # cabochaの解析結果を成型(1)
# # sentence_list >> chunk_list >> Chunk object >> Morph object
# sentence_list = []
# chunk_list = []
# morph_list = []
# dst_list = []
# # count = 0
# with open(rel_path('../data/neko.txt.cabocha')) as source_f:
#     iter_source_f = iter(source_f)  # iterable(I/Oobject)からiteratorを作る。
#     parsed = iter_source_f.next()
#     while True:
#         # count += 1
#         # if count > 100: break
#         if parsed == 'EOS\n':
#             for i, dst in enumerate(dst_list):
#                 chunk_list[i].dst = dst
#                 if dst >= 0: chunk_list[dst].src.append(i)
#             sentence_list.append(chunk_list)
#             # del(chunk_list[:])   del関数は指定したmutableなobjectの使用メモリを解放してしまうので挙動がおかしくなる。
#             chunk_list = []
#             dst_list = []
#             try:
#                 parsed = iter_source_f.next()
#             except StopIteration:
#                 break
#         elif parsed[:2] == '* ':
#             dst_list.append(int(parsed.split()[2].rstrip('D')))
#             parsed = iter_source_f.next()
#             while parsed != 'EOS\n' and parsed[:2] != '* ':
#                 morph = re.split(r'[\t,]', parsed)
#                 morph_list.append(Morph(morph[0], morph[7], morph[1], morph[2]))
#                 parsed = iter_source_f.next()
#             chunk_list.append(Chunk(morph_list))
#             morph_list = []
#         else:
#             print('improper input')
#             break



# cabochaの解析結果を成型(2)
# sentence_list >> chunk_list >> Chunk object >> Morph object
sentence_list = []
chunk_dict = {}
# count = 0
with open(rel_path('../data/neko.txt.cabocha')) as source_f:
    for parsed in source_f:
        # count += 1
        # if count > 150: break
        if parsed == 'EOS\n':
            sentence_list.append([m for i, m in sorted(chunk_dict.items(), key = lambda c: c[0])])
            chunk_dict.clear()
        elif parsed[:2] == '* ':
            col = parsed.split()
            idx = int(col[1])
            dst = int(col[2].rstrip('D'))
            if idx not in chunk_dict:
                chunk_dict[idx] = Chunk()
            chunk_dict[idx].dst = dst
            if dst >= 0:
                if dst not in chunk_dict:
                    chunk_dict[dst] = Chunk()
                chunk_dict[dst].src.append(idx)
        else:
            morph = re.split(r'[\t,]', parsed)
            chunk_dict[idx].morphs.append(Morph(morph[0], morph[7], morph[1], morph[2]))


# 出力
for i, sentence in enumerate(sentence_list, 1):
    if i == 8:
        for chunk in sentence:
            print(chunk)
        break
