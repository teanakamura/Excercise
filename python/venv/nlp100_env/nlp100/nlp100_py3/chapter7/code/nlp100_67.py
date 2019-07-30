"""
67. 複数のドキュメントの取得
特定の（指定した）別名を持つアーティストを検索せよ．
"""

from pymongo import MongoClient
from pprint import pprint
from bson.regex import Regex
import sys

def search_with_alias(collection, name, *, perfect_match=False):
    if perfect_match:
        for hit in collection.find({ 'aliases.name': name }):
            yield hit
    else:
        for hit in  collection.find({ 'aliases.name': Regex(name) }):
            yield hit

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    collection = client.nlp100.artists
    try:
        name = sys.argv[1]
    except IndexError:
        print('what is the search term?')
        sys.exit()
    perfect_match = int(sys.argv[2]) if len(sys.argv) > 2 else True  # 第三引数として0を渡すと部分一致検索になる。
    for hit in search_with_alias(collection, name, perfect_match=perfect_match):
        pprint(hit)
