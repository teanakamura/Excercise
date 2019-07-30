"""
76. ラベル付け
学習データに対してロジスティック回帰モデルを適用し，正解のラベル，予測されたラベル，予測確率をタブ区切り形式で出力せよ．
"""


from mymodule.path_helpers import get_rel_path_from_working_directory
import numpy as np
from stemming.porter2 import stem
from nlp100_73 import sigmoid, create_x_y_data
from IPython import embed


if __name__ == '__main__':
    features_file = get_rel_path_from_working_directory(__file__, '../data/features.txt')
    source_file = get_rel_path_from_working_directory(__file__, '../data/sentiment.txt')
    theta_file = get_rel_path_from_working_directory(__file__, '../data/theta.npy')
    with open(features_file) as f:
        features = f.read().split()
    with open(source_file) as f:
        sentences = f.readlines()
    theta = np.load(theta_file)
    X, Y = create_x_y_data(sentences, features)
    predictions = sigmoid(X, theta)
    incorrect_count = 0
    incorrect_probability = 0.0
    for pred, y in zip(predictions, Y):
        correct_label = '+1' if y == 1 else '-1'
        if pred > 0.5:
            predicted_label = '+1'
            probability = pred
        else:
            predicted_label = '-1'
            probability = 1 - pred
        print('correct:%s  \tprediction:%s \tprobability:%f' % (correct_label, predicted_label, probability))

        if correct_label != predicted_label:
            incorrect_count += 1
            incorrect_probability += probability
    print('%d sentences of %d is incorrect' % (incorrect_count, len(Y)))
    print('average probability of incorrect predictions is %f' % (incorrect_probability / incorrect_count))
