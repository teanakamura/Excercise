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

pattern = r'\[\[Category.*\]\]'
categories = re.findall(pattern, extract_UK())    # pattern.findall(extract_UK()) でも同じ
for category in categories:
    print(category)
# text = extract_UK().split('\n')
# for line in text:
#     if re.search(pattern, line):   # pattern.search(line) でも同じ
#         print(line)
