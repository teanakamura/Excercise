"""
64. MongoDBの構築
アーティスト情報（artist.json.gz）をデータベースに登録せよ．さらに，次のフィールドでインデックスを作成せよ: name, aliases.name, tags.value, rating.value
"""

from IPython import embed
from pymongo import MongoClient, IndexModel
from mymodule.path_helpers import get_rel_path_from_working_directory
import json

def create_db(json_file_path, collection):
    with open(json_file_path) as f:
        data_dic = {}
        for i, line in enumerate(f, 1):
            data = json.loads(line)
            id = data['id']
            data_dic[id] = data
            print('finish %d rows.' % (i), end = '\r')  # consoleに上書き出力
        else:
            print()
            data_arr = list(data_dic.values())
            max_arr_size = 100000
            for j, data_sub_arr in enumerate(split_list(data_arr, max_arr_size)):
                print('store %d-%d data' % (j * max_arr_size, (j + 1) * max_arr_size))
                collection.insert_many(data_sub_arr)

def split_list(l, n):
    """
    リストをサブリストに分割する
    :param l: リスト
    :param n: サブリストの要素数
    :return:
    """
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]

def create_indexes(collection, index_keys, option=None):
    params = [IndexModel([item]) for item in index_keys.items()]
    collection.create_indexes(params)

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.nlp100
    collection = db.artists
    collection.drop()
    json_file = get_rel_path_from_working_directory(__file__, '../data/artist.json')
    create_db(json_file, collection)
    index_keys = {'name': 1, 'aliases.name': 1, 'tags.value': 1, 'rating.value': 1}
    create_indexes(collection, index_keys)
