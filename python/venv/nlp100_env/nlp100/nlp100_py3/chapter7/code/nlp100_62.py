"""
62. KVS内の反復処理
60で構築したデータベースを用い，活動場所が「Japan」となっているアーティスト数を求めよ．
"""

import redis
import sys
import random
import time
from IPython import embed

def number_of_artists_who_play_in_japan(r):
    search_value = 'Japan'.encode('utf-8')
    # num = len([1 for key in r.keys() if r.get(key) == search_value ]) # 遅い
    # num = [r.get(key) for key in r.keys()].count(search_value) # 遅い

    # i = 0  # 遅い
    # for key in r.keys():
    #     if r.get(key) == search_value:
    #         i += 1
    #         sys.stdout.write('\r%d' % i)

    keys = r.keys()
    values = r.mget(keys) # 今回はkeysのサイズが1024**2以下なのでまとめて送れる。
    return values.count(search_value)

if __name__ == '__main__':
    # r = redis.Redis(host='localhost', port=6379, db=0)
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    num = number_of_artists_who_play_in_japan(r)
    print(num)
