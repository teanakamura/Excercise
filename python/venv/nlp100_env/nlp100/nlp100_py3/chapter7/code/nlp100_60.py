"""
60. KVSの構築
Key-Value-Store (KVS) を用い，アーティスト名（name）から活動場所（area）を検索するためのデータベースを構築せよ．
"""

# from IPython import embed
from mymodule.path_helpers import get_rel_path_from_working_directory
import json
import redis
import sys


def _create_name_area_kvs(json_file_path):
    """
    同じartistが複数回出てくることもあるので、最後に出てきたrowにareaがなければNoneになってしまう。
    """
    with open(json_file_path) as f:
        dic = {}
        mapping_num = 0
        mapping_size = 1024 ** 2 / 2 - 1  # redis commandに渡せる引数の最大数
        for i, line in enumerate(f, 1):
            data = json.loads(line)
            name = data.pop('name')
            area = data.pop('area', 'None')
            dic[name] = area
            if i == mapping_num * mapping_size + 1:
                if i != 1:
                    print('')
                    r.mset(dic)
                dic = {}
                print('%d - %dth line' % (mapping_num * mapping_size + 1, (mapping_num + 1) * mapping_size))
                mapping_num += 1
            sys.stdout.write('\r%d' % i)   # consoleに上書き出力
        else:
            r.mset(dic)
            print('')


def create_name_area_kvs(json_file_path):
    with open(json_file_path) as f:
        dic = {}
        counter = 1
        max_dic_size = 1024 ** 2 // 2 - 1  # redis commandに渡せる引数の最大数
        names_with_data = set()
        names_without_data = set()
        with_data_num = 0
        for i, line in enumerate(f, 1):
            data = json.loads(line)
            name = data.pop('name')
            area = data.pop('area', None)
            if area:
                dic[name] = area
                names_with_data.add(name)
                with_data_num += 1
            else:
                names_without_data.add(name)
            if with_data_num == counter * max_dic_size:
                print('\nsetting data with area info to redis.')
                r.mset(dic)
                dic = {}
                counter += 1
            sys.stdout.write('\rfinish %d rows, and %d rows have area info.' % (i, with_data_num))  # consoleに上書き出力
        else:
            print('\nsetting data with area info to redis.')
            r.mset(dic)
            name_list_without_data = list(names_without_data - names_with_data)
            with_data_num = len(names_with_data)
            without_data_num = len(name_list_without_data)
            i = 0
            while True:
                partial_name_list_without_data = name_list_without_data[i * max_dic_size: (i+1) * max_dic_size]
                if not partial_name_list_without_data: break
                dic = {name: 'None' for name in partial_name_list_without_data}
                print('setting data without area info to redis.')
                r.mset(dic)
                i += 1
            print('all %d artists, %d artists have area info, %d artists have no area info.' % (with_data_num + without_data_num, with_data_num, without_data_num))


if __name__ == '__main__':
    # r = redis.Redis(host='localhost', port=6379, db=0)
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    r.flushall()
    json_file = get_rel_path_from_working_directory(__file__, '../data/artist.json')
    create_name_area_kvs(json_file)
