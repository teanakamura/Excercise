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
    def surface_no_symbol(self):
        return ''.join([m.surface for m in self.morphs if m.pos != '記号'])
    def surface_masked(self, pos, mask, cutoff=False):
        #return ''.join([mask if m.pos == pos else m.surface for m in self.morphs])
        """
        記号は消去。名詞が連続する場合は先頭のみをmaskして残りは消去。
        cutoff=True のときは一つ目の名詞までを返す。
        """
        string = ''
        top = True
        for m in self.morphs:
            if m.pos == '名詞' and top:
                string += mask
                if cutoff: return string
                top = False
            elif m.pos == '名詞':
                pass
            elif m.pos == '記号':
                pass
                top = True
            else:
                string += m.surface
                top = True
        return string


# get relative path from working directory
def rel_path(rel_path_from_this_file):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path_from_this_file))


def search_root_path(i, sentence):
    if sentence[i].dst == -1:
        return [i]
    else:
        return [i] + search_root_path(sentence[i].dst, sentence)


def search_intermedial_path(x, y ,sentence):
    x_root = search_root_path(x, sentence)
    y_root = search_root_path(y, sentence)
    if y in x_root:
        return x_root[:x_root.index(y) + 1]
    elif x in y_root:
        return y_root[:y_root.index(x) + 1]
    else:
        k = -1
        while True:
            if x_root[k-1] == y_root[k-1]:
                k -= 1
            else:
                return x_root[:k], y_root[:k], x_root[k]

# cabochaの解析結果を成型
# sentence_list >> chunk_list >> Chunk object >> Morph object
sentence_list = []
chunk_dict = {}
# count = 0
with open(rel_path('../data/neko.txt.cabocha')) as source_f:
    for parsed in source_f:
        # count += 1
        # if count > 1500: break
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


# 出力（名詞ベース）
for i, sentence in enumerate(sentence_list, 1):
    if i < 20:
        print('\n%d文目' % i)
        noun_chunks = [i for i, chunk in enumerate(sentence) if '名詞' in [m.pos for m in chunk.morphs]]
        #print(noun_chunks)
        for i in range(len(noun_chunks)):
            x = noun_chunks[i]
            for j in range(i+1, len(noun_chunks)):
                y = noun_chunks[j]
                #print('i:%d, j:%d, x:%d, y:%d' % (i, j, x, y))
                path = search_intermedial_path(x, y, sentence)
                if isinstance(path, tuple):
                    x_path, y_path, common = path
                    x_str = ' -> '.join([sentence[x_path[0]].surface_masked('名詞', 'X')] \
                            + [sentence[i].surface_no_symbol() for i in x_path[1:]])
                    y_str = ' -> '.join([sentence[y_path[0]].surface_masked('名詞', 'Y')] \
                            + [sentence[i].surface_no_symbol() for i in y_path[1:]])
                    common_str = sentence[common].surface_no_symbol()
                    print('%s | %s | %s' % (x_str, y_str, common_str))
                else:
                    all_str = ' -> '.join([sentence[path[0]].surface_masked('名詞', 'X')] \
                            + [sentence[i].surface_no_symbol() for i in path[1:-1]] \
                            + [sentence[path[-1]].surface_masked('名詞', 'Y', True)])
                    print(all_str)
    elif i >= 9:
        break
