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


# 出力(2) src の文節１つに助詞が複数含まれる場合は最後のもののみを出力する。
with open(rel_path('../data/case_pattern.txt'), 'w') as write_f:
    for sentence in sentence_list:
        for chunk in sentence:
            try:
                # verb = chunk.morphs[[m.pos for m in chunk.morphs].index('動詞')].base  この場合 except はValueError
                verb = [m.base for m in chunk.morphs if m.pos == '動詞'][0]
                particles = []
                for src in chunk.src:
                    particles.extend([m.base for m in sentence[src].morphs if m.pos == '助詞'][-1:])
                            # [-1:]をextendする代わりに、[-1]をappendしてもよいが、空リストの場合にerrorとなるのでtryなどで処理してやる必要が生じる。
                            # [-1:]をappendするとlistのlistとなってしまってめんどくさい。
                if len(particles) > 0:
                    print(verb + '\t' + ' '.join(particles))
                    write_f.write(verb + '\t' + ' '.join(particles) + '\n')
            except IndexError:
                pass


'''
後半の課題を見る限り、一文ずつの結果を記録すべき。
以下は文書全体でcollections.Counter を用いて結果を出力したもの。

from collections import Counter

# 格パターンの辞書を作成
case_pattern_dict = {}
for sentence in sentence_list:
    for chunk in sentence:
        try:
            index =  [m.pos for m in chunk.morphs].index('動詞')
            verb = chunk.morphs[index].base
            if verb not in case_pattern_dict:
                case_pattern_dict[verb] = Counter()
            case_pattern_dict[verb].update([m.base for src in chunk.src for m in sentence[src].morphs if m.pos == '助詞'])
        except ValueError:
            pass

# 出力
for verb, particle_counter in sorted(case_pattern_dict.items()):
    try:
        print(verb + '\t' + ' '.join(list(zip(*particle_counter.most_common())[0])))
    except IndexError:
        pass
'''


'''
Unix command
1.
    $ sort ./chapter5/data/case_pattern.txt | uniq -c | sort -nrk1 | head -10
            # これだと同じ動詞と助詞の組み合わせでも、他の助詞によって別の組み合わせと判断されてしまうので以下
    $ awk '{for(i=2; i <= NF; i++){print $1, $i}}' ./chapter5/data/case_pattern.txt | sort | uniq -c | sort -nrk1 | head -10
2.
    $ awk '{if($1 == "する"){for(i=2; i <= NF; i++){print $1, $i}}}' ./chapter5/data/case_pattern.txt | sort | uniq -c | sort -nrk1
    $ awk '{if($1 ~ "^する.*"){for(i=2; i <= NF; i++){print $1, $i}}}' ./chapter5/data/case_pattern.txt | sort | uniq -c | sort -nrk1

    # 注意
    # 上の条件式では == を使用。シェルスクリプトでは = と == は等価らしいが awk コマンドでは区別されているらしく、= は代入になるので注意。以下を実行することで確かめられる。
    $ awk '{print $1; if($1 = "する"){for(i=2; i <= NF; i++){print NR, i}}}' ./chapter5/data/case_pattern.txt
    $ awk '{print $1; if($1 == "する"){for(i=2; i <= NF; i++){print NR, i}}}' ./chapter5/data/case_pattern.txt
'''
