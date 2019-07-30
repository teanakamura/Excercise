#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import json
import re
import urllib
import urllib2
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
    result = {info[0]:info[1] for info in base_infoes}  # dictの内包表記
    order = [info[0] for info in base_infoes]  # k# dict型は順番が追加順でないので出力順を調整して確認しやすくするにeyの順番を保存するための変数を用意する。listの内包表記
    return result, order

def remove_mediawiki_markup(string):
    pattern1 = r'(\'{2,5})(.+?)(\1)'   # 強調３種
    pattern2 = ur'(?<!REDIRECT)\[\[(?!ファイル:|File:|Category:).*?\|?([^|]+?)\]\]'  # 内部リンク
    pattern3 = ur'\[\[(ファイル|File|Category):.+\]\]'  # ファイルとカテゴリ
    pattern4_1 = r'\[(http[^ ]+)]'  # 外部リンク1
    pattern4_2 = r'\[http[^ ]+\s?(.*)\]'  # 外部リンク2
    pattern5 = r'<.+>'  # HTMLタグ
    pattern6 = re.compile(r'^(={2,5})(.+)(\1)', re.M)  # 見出し
    pattern7 = re.compile(r'^(?:\*{1,2}|#{1,2}|(?:;|:)?)(.+)', re.M)  # 各種箇条書き
    pattern8 = r'\{\{lang\|.+\|(.*)\}\}'  #言語指定

    string = re.sub(pattern1, r'\2', string)
    string = re.sub(pattern2, r'\1', string)
    string = re.sub(pattern3, '', string)
    string = re.sub(pattern4_1, r'\1', string)
    string = re.sub(pattern4_2, r'\1', string)
    string = re.sub(pattern5, '', string)
    string = re.sub(pattern6, r'\2', string)
    string = re.sub(pattern7, r'\1', string)
    string = re.sub(pattern8, r'\1', string)
    return string

# urlの作成
text = extract_UK()
result, order = extract_baseinfo(text)
filename = remove_mediawiki_markup(result[u'国旗画像'])
parsed_filename = urllib.quote(filename)
query = '&titles=File:' + parsed_filename\
            +'&prop=imageinfo'\
            '&iiprop=url'
url = 'https://www.mediawiki.org/w/api.php'\
        '?action=query' + query\
        + '&format=json'

# MediaWikiのサービスへリクエスト送信
request = urllib2.Request(url,headers={'User-Agent': 'NLP100_Python'})
connection = urllib2.urlopen(request)

# jsonとして受信
data = json.loads(connection.read().decode())
print(data['query']['pages']['-1']['imageinfo'][0]['url'])


"""
urlの必要項目はmediawikiの公式を参考
titlesについてはFile:をつけてそれ以降はエスケープ処理した
mdeiawikiではUser-Agent headerを必須とするらしいのでrequestの作成の際に付与した
しかし、urlopenへ渡すのはrequestオブジェクトでもurlの文字列でもよいのだが、User-Agent headerを付与していないurlでも正常な結果が得られた。
"""
