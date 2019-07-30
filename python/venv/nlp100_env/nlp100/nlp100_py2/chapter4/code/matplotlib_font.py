#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.font_manager as fm

# matplotlib 初期化ファイルの場所
print(mpl.__file__)

# matplotlib 設定ファイルmatplotlibrc の場所
print(mpl.matplotlib_fname())

# matplotlib 現在の font familly
print(mpl.rcParams['font.family'])  # font family名

# システム上の font 一覧
print(fm.findSystemFonts(fontpaths=None, fontext='ttf'))

# フォント適用時に指定できるフォント名一覧
print([f.name for f in fm.fontManager.ttflist])

#デフォルトでのフォントを変更したいときは matplotlibrc ファイル の font.family の部分を変更する。
