"""
61. KVSの検索
60で構築したデータベースを用い，特定の（指定された）アーティストの活動場所を取得せよ．
"""

import redis
import sys
import random

def search_area_from_name(redis):
    if len(sys.argv) == 1:
        print('活動場所を検索したいartistのnameを入力してください。')
        sys.argv.append(input())
    name = sys.argv[1].encode('utf-8')
    if name == b'random':
        # name = random.choice(redis.keys())
        name = redis.randomkey()
    area = redis.get(name)
    name = name.decode('utf-8')
    if area == b'None':
        print('%sの活動場所は未登録です。' % name)
    elif area == None:
        print('%sというartistは未登録です。' % name)
    else:
        print('%sの活動場所は%sです。' % (name, area.decode('utf-8')))

if __name__ == '__main__':
    # r = redis.Redis(host='localhost', port=6379, db=0)
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    search_area_from_name(r)
