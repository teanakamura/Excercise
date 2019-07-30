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
    def chunk_surface_without_symbol(self):
        return ''.join([m.surface for m in self.morphs if m.pos != '記号'])


# get relative path from working directory
def rel_path(rel_path_from_this_file):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path_from_this_file))


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
with open(rel_path('../data/sahen.txt'), 'w') as output_f:
    for sentence in sentence_list:
        for i, chunk in enumerate(sentence):
            if len(chunk.morphs) == 2 and \
                    chunk.morphs[0].pos1 == 'サ変接続' and \
                    chunk.morphs[1].pos == '助詞' and \
                    chunk.morphs[1].base == 'を':
                try:
                    dst_chunk = sentence[chunk.dst]
                    predicate = chunk.chunk_surface_without_symbol() + [m.base for m in dst_chunk.morphs if m.pos == '動詞'][0]
                    src_list = dst_chunk.src + chunk.src
                    src_list.remove(i)
                    particles = []
                    for src in src_list:
                        # particles.extend([[m.base, sentence[src].chunk_surface_without_symbol()] \
                        #         for m in sentence[src].morphs if m.pos == '助詞'][-1:])
                        try:
                            particles.append([
                                    [m.base for m in sentence[src].morphs if m.pos == '助詞'][-1],
                                    sentence[src].chunk_surface_without_symbol()])
                        except IndexError:
                            pass
                    if len(particles) > 0:
                        particles_m, particles_c = zip(*particles)
                        print('%s\t%s\t%s' % (predicate, ' '.join(particles_m), ' '.join(particles_c)))
                        output_f.write('%s\t%s\t%s\n' % (predicate, ' '.join(particles_m), ' '.join(particles_c)))
                except IndexError:
                    # print(chunk.chunk_surface_without_symbol() + sentence[chunk.dst].chunk_surface_without_symbol())
                    pass


# # 出力（動詞ベース）
# with open(rel_path('../data/sahen.txt'), 'w') as output_f:
#     for sentence in sentence_list:
#         for chunk in sentence:
#             try:
#                 verb = [m.base for m in chunk.morphs if m.pos == '動詞'][0]
#                 predicate = ''
#                 particles = []
#                 src_list = chunk.src
#                 for src in src_list:
#                     src_chunk = sentence[src]
#                     if len(src_chunk.morphs) == 2 and \
#                                 src_chunk.morphs[0].pos1 == 'サ変接続' and \
#                                 src_chunk.morphs[1].pos == '助詞' and \
#                                 src_chunk.morphs[1].base == 'を':
#                         predicate = src_chunk.chunk_surface_without_symbol() + verb
#                         src_list.extend(src_chunk.src)
#                     else:
#                         #  particles.extend([[m.base, sentence[src].chunk_surface_without_symbol()] \
#                         #         for m in sentence[src].morphs if m.pos == '助詞'][-1:])
#                         try:
#                             particles.append([
#                                     [m.base for m in src_chunk.morphs if m.pos == '助詞'][-1],
#                                     src_chunk.chunk_surface_without_symbol()])
#                         except IndexError:
#                             pass
#                 if len(predicate) > 0 and len(particles) > 0:
#                     particles_m, particles_c = zip(*particles)
#                     print('%s\t%s\t%s' % (predicate, ' '.join(particles_m), ' '.join(particles_c)))
#                     output_f.write('%s\t%s\t%s\n' % (predicate, ' '.join(particles_m), ' '.join(particles_c)))
#             except IndexError :
#                 pass


"""
Unix command
1.
    $ awk '{print $1}' ./chapter5/data/sahen.txt | sort | uniq -c | sort -nrk1 | head -10
    $ cut -f1 ./chapter5/data/sahen.txt | sort | uniq -c | sort -nrk1 | head -10
2.
    $ awk -F'[\t]' '{print $1, $2}' ./chapter5/data/sahen.txt | awk '{for(i=2; i <= NF; i++){print $1, $i}}' | sort | uniq -c | sort -nrk1 | head -10
    $ cut -f1,2 ./chapter5/data/sahen.txt | awk '{for(i=2; i <= NF; i++){print $1, $i}}' | sort | uniq -c | sort -nrk1 | head -10
    デフォルトのデリミタはawkコマンドが各種空白文字で、cutコマンドはtab。
