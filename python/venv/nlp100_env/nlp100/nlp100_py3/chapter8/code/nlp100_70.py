"""
70. データの入手・整形
文に関する極性分析の正解データを用い，以下の要領で正解データ（sentiment.txt）を作成せよ．

rt-polarity.posの各行の先頭に"+1 "という文字列を追加する（極性ラベル"+1"とスペースに続けて肯定的な文の内容が続く）
rt-polarity.negの各行の先頭に"-1 "という文字列を追加する（極性ラベル"-1"とスペースに続けて否定的な文の内容が続く）
上述1と2の内容を結合（concatenate）し，行をランダムに並び替える
sentiment.txtを作成したら，正例（肯定的な文）の数と負例（否定的な文）の数を確認せよ．
"""

from mymodule.path_helpers import get_rel_path_from_working_directory
from IPython import embed
from random import shuffle


def detect_file_encoding(file_path):
    with open(file_path, mode='rb') as f:
        binary = f.read()
        import chardet
        print(chardet.detect(binary))


def count_sentiment_sentences(file_path):
    pos_count = 0
    neg_count = 0
    with open(file_path,  encoding='Windows-1252') as f:
        for line in f:
            if line.startswith('+1 '):
                pos_count += 1
            elif line.startswith('-1 '):
                neg_count += 1
            else:
                raise Exception
    return pos_count, neg_count


if __name__ == '__main__':
    pos_file = get_rel_path_from_working_directory(__file__, '../data/rt-polaritydata/rt-polaritydata/rt-polarity.pos')
    neg_file = get_rel_path_from_working_directory(__file__, '../data/rt-polaritydata/rt-polaritydata/rt-polarity.neg')
    # detect_file_encoding(pos_file)
    res_list = []
    with open(pos_file, encoding='Windows-1252') as f:
        res_list.extend(['+1 ' + line for line in f])
    with open(neg_file, encoding='Windows-1252') as f:
        res_list.extend(['-1 ' + line for line in f])
    shuffle(res_list)

    output_file = get_rel_path_from_working_directory(__file__, '../data/sentiment.txt')
    with open(output_file, 'w') as f:
        f.write(''.join(res_list))
    print('sentiment.txt file is made.')

    pos_count, neg_count = count_sentiment_sentences(output_file)
    print('pos_count: %d, neg_count: %d' % (pos_count, neg_count))
