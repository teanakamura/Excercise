"""
71. ストップワード
英語のストップワードのリスト（ストップリスト）を適当に作成せよ．さらに，引数に与えられた単語（文字列）がストップリストに含まれている場合は真，それ以外は偽を返す関数を実装せよ．さらに，その関数に対するテストを記述せよ．
"""


from mymodule.path_helpers import get_rel_path_from_working_directory
from IPython import embed

def check_stems_dict_from_sentences(sentences):
    from stemming.porter2 import stem
    from pprint import pprint
    stems_dict = {}
    for s in sentences:
        for w in s.split():
            stemmed_word = stem(w)
            stems_dict[stemmed_word] = 1 if stemmed_word not in stems_dict else stems_dict[stemmed_word] + 1
    sorted_stems_dict = sorted(stems_dict.items(), key=lambda x: x[1])
    pprint(sorted_stems_dict)


stopwords = '. the , a and of it to is that in as but with this for an be on you not by one more about are has at from than have " all -- his so if or what i too there who just into will can'.split()
"""
与えられた文章群から単語分割してステミングして出現回数順に並べたものから目視でピックアップ。
映画に関する文章なので映画に関連する語も上位に出現したがそれはストップワードではないので除外。
"""


def is_stopword(word):
    from stemming.porter2 import stem
    return stem(word.lower()) in stopwords


if __name__ == '__main__':
    file_path = get_rel_path_from_working_directory(__file__, '../data/sentiment.txt')
    with open(file_path,  encoding='Windows-1252') as f:
        sentences = f.readlines()
    check_stems_dict_from_sentences(sentences)
