#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import CaboCha

# get relative path from working directory
def rel_path(rel_path_from_this_file):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path_from_this_file))

with open(rel_path('../../chapter4/data/neko.txt')) as source_f:
    with open(rel_path('../data/neko.txt.cabocha'), 'w') as output_f:
        cabocha_parser = CaboCha.Parser('')
        # parsed = cabocha_parser.parse(source_f.read).toString(CaboCha.FORMAT_LATTICE)
        # output_f.write(parsed)
            # # この手法だと文の境界の判定ができない。
        for line in source_f:
            parsed = cabocha_parser.parse(line).toString(CaboCha.FORMAT_LATTICE)
            output_f.write(parsed)
