"""
65. MongoDBの検索
MongoDBのインタラクティブシェルを用いて，"Queen"というアーティストに関する情報を取得せよ．さらに，これと同様の処理を行うプログラムを実装せよ．
"""

from pymongo import MongoClient
from pprint import pprint
from bson.regex import Regex

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    collection = client.nlp100.artists
    
    # # perfect match
    # for i, hit in enumerate(collection.find({ 'name': 'Queen' }), 1):
    #     print(i, end='番目のヒット\n')
    #     pprint(hit)

    # partial match
    for i, hit in enumerate(collection.find({ 'name': Regex('Queen') }), 1):
        print(i, end='番目のヒット\n')
        pprint(hit)

"""mongoのインタラクティブシェルでの実行
mongoでshell起動して、
show dbsでdbを検索して
use <db>でdb移動して
show collectionsでcollectionを検索して
db.<collection>.find({ name: 'Queen' })
db.<collection>.find({ name: /Queen/ })
"""
