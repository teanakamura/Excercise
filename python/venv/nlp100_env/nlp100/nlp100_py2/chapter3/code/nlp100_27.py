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

def extract_baseinfo(text):
    pattern1 = ur'{{基礎情報(?:(?:[^{}]*{{[^{]+}})*[^{]*)}}'
    pattern2 = re.compile(r'\|(.+?)\s*=[\t\r\f\v]*(.*?)(?=\n\||\n\}\})', re.DOTALL)
    all_base_info = re.findall(pattern1, text)
    base_infoes = re.findall(pattern2, all_base_info[0])
    result = {info[0]:re.sub(r'<.+>', '', info[1]) for info in base_infoes}  # dictの内包表記
    order = [info[0] for info in base_infoes]  # k# dict型は順番が追加順でないので出力順を調整して確認しやすくするにeyの順番を保存するための変数を用意する。listの内包表記
    return result, order

def remove_emphatic_expression(string):
    return re.sub(r'(\'{2,5})(.+?)(\1)', r'\2', string)

def replace_linked_expression(string):
    #patter = re.compile(u'\[\[.*?\|?([^|]+?)\]\]')
    pattern = ur'(?<!REDIRECT)\[\[(?!ファイル:|File:|Category:).*?\|?([^|]+?)\]\]'
        # REDIRECT、ファイル、Categoryにはマッチしないように調整
        # (?<!regex) は否定あと読みアサーション、(?!regex) は否定先読みアサーション
        # "ファイル"にマッチするようにuは必須。re.sub関数でrを使ってpattern宣言するのはできない。"
    return re.sub(pattern, r'\1', string)

text = extract_UK()
text = remove_emphatic_expression(text)
text = replace_linked_expression(text)
    # まとめて置き換え処理するのはよいが、これだと不要な部分まで置き換え処理するので、問題28のように抽出した後に置き換え処理した方が良い。
result, order = extract_baseinfo(text)
for key in order:
    print(key + ":" + result[key])
