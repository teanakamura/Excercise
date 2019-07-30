"""
63. オブジェクトを値に格納したKVS
KVSを用い，アーティスト名（name）からタグと被タグ数（タグ付けされた回数）のリストを検索するためのデータベースを構築せよ．さらに，ここで構築したデータベースを用い，アーティスト名からタグと被タグ数を検索せよ．
"""

from IPython import embed
from mymodule.path_helpers import get_rel_path_from_working_directory
import json
import redis
import sys

def _create_name_tags_kvs(json_file_path, r):
    """
    同名のartistが複数回出てくることもあるので、tagsがある時とない時が存在するとデータ型が異なるのでredisのエラーとなる。
    """
    with open(json_file_path) as f:
        has_data_num = 0
        no_data_num = 0
        counter = 1
        max_args_size = 1024 ** 2 / 2 - 1
        names_without_data = {}
        for i, line in enumerate(f, 1):
            data = json.loads(line)
            name = data.pop('name')
            tags = data.pop('tags', None)
            if tags:
                if i > 563235:
                    embed()
                mapping = { tag['value']: tag['count'] for tag in tags }
                r.hmset(name, mapping)
                has_data_num += 1
            else:
                names_without_data[name] = 'None'
                no_data_num  += 1
            if no_data_num == max_args_size * counter:
                r.mset(names_without_data)
                names_without_data = {}
                counter += 1
            sys.stdout.write('\rfinish %d data, and %d data have tags.' % (i, has_data_num))  # consoleに上書き出力
        else:
            r.mset(names_without_data)
            print('')

def create_name_tags_kvs(json_file_path, r):
    with open(json_file_path) as f:
        with_data_num = 0
        counter = 1
        max_dic_size = 1024 ** 2 // 2 - 1
        names_with_data = set()
        names_without_data = set()
        for i, line in enumerate(f, 1):
            data = json.loads(line)
            name = data.pop('name')
            tags = data.pop('tags', None)
            if tags:
                mapping = { tag['value']: tag['count'] for tag in tags }
                names_with_data.add(name)
                r.hmset(name, mapping)
                with_data_num += 1
            else:
                names_without_data.add(name)
            sys.stdout.write('\rfinish %d rows, and %d rows have tags info.' % (i, with_data_num))  # consoleに上書き出力
        else:
            name_list_without_data = list(names_without_data - names_with_data)
            with_data_num = len(names_with_data)
            without_data_num = len(name_list_without_data)
            print ('\nsetting data without tags info to redis.')
            i = 0
            while True:
                partial_name_list_without_data = name_list_without_data[i * max_dic_size : (i+1) * max_dic_size]
                if not partial_name_list_without_data: break
                dic = { name: 'None' for name in partial_name_list_without_data }
                r.mset(dic)
                i += 1
            print('all %d artists, %d artists have tags info, %d artists have no tags info.' % (with_data_num + without_data_num, with_data_num, without_data_num))

if __name__ == '__main__':
    # r = redis.Redis(host='localhost', port=6379, db=0)
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.flushall()
    json_file = get_rel_path_from_working_directory(__file__, '../data/artist.json')
    create_name_tags_kvs(json_file, r)
