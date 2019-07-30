#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import json
import re
import os

# get relative path from working directory
def rel_path(rel_path_from_this_file):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path_from_this_file))

def extract_UK():
    with gzip.open(rel_path('../data/jawiki-country.json.gz')) as f:
        for line in f:
            doc = json.loads(line)
            if doc['title'] == u'イギリス':
                return doc['text']

# 手法1.1
pattern = re.compile(r'\[\[Category:(.+?)(\|.*)?\]\]')
categories = re.findall(pattern, extract_UK())    # pattern.findall(extract_UK()) でも同じ
for category in categories:
    print(category[0])   # re.findall ではpatternに()がある場合はその中身がリスト形式で保存される。

# 手法1.2
pattern = re.compile(r'\[\[Category:(.+?)(?:\|.*)?\]\]')  # (?:regex) とした場合はこの内部は参照には使用できないことを示す
categories = re.findall(pattern, extract_UK())    # pattern.findall(extract_UK()) でも同じ
for category in categories:
    print(category)

# 手法2
pattern = re.compile(r'\[\[Category:(.+?)(\|.*)?\]\]')
text = extract_UK().split('\n')
for line in text:
    if re.search(pattern, line):   # pattern.search(line) でも同じ
        print(re.sub(pattern, r'\1', line))  # pattern の()内の正規表現にマッチした文字列は \num でアクセスできる。
