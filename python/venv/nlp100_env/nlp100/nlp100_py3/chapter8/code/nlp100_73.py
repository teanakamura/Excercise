"""
73. 学習
72で抽出した素性を用いて，ロジスティック回帰モデルを学習せよ．
"""

from mymodule.path_helpers import get_rel_path_from_working_directory
import numpy as np
from stemming.porter2 import stem
from IPython import embed


def update_theta(eta, x, y, theta):
    return theta + eta * np.dot(y - sigmoid(x, theta), x)

def sigmoid(x, theta):
    return 1 / (1 + np.exp(-np.dot(x, theta)))

def create_x_y_data(sentences, features):
    x_list = []
    y_list = []
    for i, s in enumerate(sentences, 1):
        print('line' + str(i), end='\r')
        words = s.split()
        y_list.append(1 if words[0] == '+1' else 0)
        stemmed_words = [stem(w) for w in words[1:]]
        x_line = [1 if f in stemmed_words else 0 for f in features]
        x_list.append(x_line)
    x = np.array(x_list)
    Y = np.array(y_list)
    X = add_x0_line_for_bias(x)
    return X, Y

def add_x0_line_for_bias(x):
    x0 = np.ones([x.shape[0], 1])
    return np.hstack([x0, x])

def object_and_grad(x, y, theta):
    """
    最小化する目的関数の値
    各θの最急降下法における勾配（ベクトル）
    """
    m = y.size
    h = sigmoid(x, theta)
    object = 1 / m * np.sum(-y * np.log(h) - (np.ones(m) - y) * np.log(np.ones(m) - h))
    grad = 1 / m * np.dot(h - y, x)
    return object, grad


if __name__ == '__main__':
    ETA = 1e-3
    EPOCH = 5000
    features_file = get_rel_path_from_working_directory(__file__, '../data/features.txt')
    source_file = get_rel_path_from_working_directory(__file__, '../data/sentiment.txt')
    theta_file = get_rel_path_from_working_directory(__file__, '../data/theta.npy')
    with open(features_file) as f:
        features = f.read().split()
    with open(source_file) as f:
        sentences = f.readlines()
    theta = np.random.rand(len(features) + 1)
    X, Y = create_x_y_data(sentences, features)

    for i in range(EPOCH):
        print('epoch' + str(i), end='\r')
        if i % 500 == 0 or i == EPOCH - 1 :
            obj, grad = object_and_grad(X, Y, theta)
            max_update_value = np.max(np.absolute(ETA * grad))
            print('epoch%d:   objective function value %f   max update value %.5e' % (i, obj, max_update_value))
        theta = update_theta(ETA, X, Y, theta)
    np.save(theta_file, theta)
