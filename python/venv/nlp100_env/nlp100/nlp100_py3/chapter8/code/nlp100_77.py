"""
77. 正解率の計測
76の出力を受け取り，予測の正解率，正例に関する適合率，再現率，F1スコアを求めるプログラムを作成せよ．
"""


from mymodule.path_helpers import get_rel_path_from_working_directory
import numpy as np
from nlp100_73 import sigmoid, create_x_y_data


def score(y, predictions):
    predicted_values = np.round(predictions)
    accuracy = np.sum((y - predicted_values) == 0) / len(y)
    # precision = np.sum(np.logical_and(y == 1, predicted_values == 1)) / np.sum(predicted_values == 1)
    precision = np.sum((y + predicted_values) == 2) / np.sum(predicted_values == 1)
    recall = np.sum((y + predicted_values) == 2) / np.sum(y == 1)
    f_value = 2 * recall * precision / (recall + precision)
    return accuracy, precision, recall, f_value

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
    accuracy, precision, recall, f_value = score(Y, predictions)
    print('accuracy: %f \tprecision: %f \trecall: %f \tFvalue: %f' % (accuracy, precision, recall, f_value))
