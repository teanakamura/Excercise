"""
72. 素性抽出
極性分析に有用そうな素性を各自で設計し，学習データから素性を抽出せよ．素性としては，レビューからストップワードを除去し，各単語をステミング処理したものが最低限のベースラインとなるであろう．
"""


from mymodule.path_helpers import get_rel_path_from_working_directory
from IPython import embed


def extract_features(sentences):
    """
    ・stopwrodsに含まれる語は除く。
    ・出現頻度の低い語（n < 3）は除く。学習の際に不適切な値になりやつい&数が多いので非効率的
    ・posとnegで出現数が同数ないしほぼ同数。単純に極性分析に無関係な語の可能性が高い&この文章群をそのまま学習に使うので、語の組み合わせによる意味の変化を考えない場合は学習に対して大きな影響を持たない。
    """
    from stemming.porter2 import stem
    from nlp100_71 import stopwords
    stems_dict = {}
    for s in sentences:
        sentiment = s[:2]
        added_list = [1, 1, 0] if sentiment == '+1' else [1, 0, 1]
        for w in s[3:].split():
            stemmed_word = stem(w)
            if stemmed_word in stopwords:
                continue
            elif stemmed_word not in stems_dict:
                stems_dict[stemmed_word] = added_list
            else:
                stems_dict[stemmed_word] = [a + b for a, b in zip(stems_dict[stemmed_word], added_list)]
    filtered_dict = {
            k:v for k,v in stems_dict.items()
            if v[0] > 3  # 14639 -> 4538
            and not 5/11 < v[1]/v[0] < 6/11  # 4538 -> 3893
        }
    return filtered_dict.keys()


if __name__ == '__main__':
    file_path = get_rel_path_from_working_directory(__file__, '../data/sentiment.txt')
    with open(file_path,  encoding='Windows-1252') as f:
        sentences = f.readlines()
    features = extract_features(sentences)
    output_file_path = get_rel_path_from_working_directory(__file__, '../data/features.txt')
    with open(output_file_path, encoding='Windows-1252', mode='w') as f:
        f.write(' '.join(features))
    print('features.txt file is made.')
