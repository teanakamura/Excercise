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

# セクションはマークアップ記法の見出しの階層のこと。多分
pattern = re.compile(ur'^.*(ファイル|File):(.+?)(?:\|.+)?$', re.M)
    # python2ではユニコード文字列を指定しないと u'ファイル'にマッチしない。
    # python3ではデフォルトでユニコード文字列なので気にせず全てrフラグで記述すれば良い。
files = re.findall(pattern, extract_UK())
for afile in files:
    print(afile[1])
