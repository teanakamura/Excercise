#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import json
import os

# get relative path from working directory
def rel_path(rel_path_from_this_file):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path_from_this_file))

with gzip.open(rel_path('../data/jawiki-country.json.gz')) as f:
    for line in f:
        doc = json.loads(line)
        if doc['title'] == u'イギリス':
            print(doc['text'])
            break
