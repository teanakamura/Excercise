"""
68. ソート
"dance"というタグを付与されたアーティストの中でレーティングの投票数が多いアーティスト・トップ10を求めよ．
"""

from pymongo import MongoClient
from pprint import pprint
from bson.regex import Regex
import sys

def search_with_dance_tag(collection):
    for hit in collection \
            .find(
                { 'tags.value': 'dance' },
                { '_id': 0, 'name': 1, 'rating.value': 1 }
            ).sort(
                [('rating.value', -1)]
            ).limit(10):
        yield hit

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    collection = client.nlp100.artists
    for hit in search_with_dance_tag(collection):
        pprint(hit)
