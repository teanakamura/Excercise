"""
74. 予測
73で学習したロジスティック回帰モデルを用い，与えられた文の極性ラベル（正例なら"+1"，負例なら"-1"）と，その予測確率を計算するプログラムを実装せよ．
"""


from mymodule.path_helpers import get_rel_path_from_working_directory
import numpy as np
from stemming.porter2 import stem
from nlp100_73 import sigmoid


def create_x_data(sentences, features):
    words = sentence.split()
    stemmed_words = [stem(w) for w in words]
    x_line = [1] + [1 if f in stemmed_words else 0 for f in features]
    x = np.array(x_line)
    return x

if __name__ == '__main__':
    features_file = get_rel_path_from_working_directory(__file__, '../data/features.txt')
    theta_file = get_rel_path_from_working_directory(__file__, '../data/theta.npy')
    with open(features_file) as f:
        features = f.read().split()
    theta = np.load(theta_file)
    while True:
        sentence = input('sentence: ')
        x = create_x_data(sentence, features)
        h = sigmoid(x, theta)
        if h > 0.5:
            print('label: +1 (prediction: %f)' % h)
        else:
            print('label: -1 (prediction: %f)' % (1 - h))
