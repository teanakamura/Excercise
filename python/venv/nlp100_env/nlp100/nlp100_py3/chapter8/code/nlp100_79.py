"""
79. 適合率-再現率グラフの描画
ロジスティック回帰モデルの分類の閾値を変化させることで，適合率-再現率グラフを描画せよ．
"""


from mymodule.path_helpers import get_rel_path_from_working_directory
from random import shuffle
import numpy as np
from stemming.porter2 import stem
from matplotlib import pyplot as plt
from nlp100_73 import update_theta, sigmoid, create_x_y_data, object_and_grad
from nlp100_78 import remove_no_appear_features


def drange(begin, end, step):
    n = begin
    while n+step < end:
        yield n
        n += step

def score_from_variable_threshold(threshold, y, predictions):
    predicted_values = predictions > threshold
    precision = weird_division(np.sum((y + predicted_values) == 2), np.sum(predicted_values == 1), 1)
    recall = np.sum((y + predicted_values) == 2) / np.sum(y == 1)
    return precision, recall

def weird_division(n, d, s=0):
     return n / d if d else s


if __name__ == '__main__':
    N = 5
    ETA = 1e-3
    EPOCH = 5000
    source_file = get_rel_path_from_working_directory(__file__, '../data/sentiment.txt')
    features_file = get_rel_path_from_working_directory(__file__, '../data/features.txt')
    with open(source_file,  encoding='Windows-1252') as f:
        sentences = f.readlines()
    with open(features_file) as f:
        features = f.read().split()
    shuffle(sentences)
    size = len(sentences)
    precision_list = [[] for i in range(1001)]  # 二次元配列なので [[]] * 1001 はidが同一になってまずい
    recall_list = [[] for i in range(1001)]

    for k in range(N):
        print('Learning%d' % k)
        training_sentences = sentences[:round(k / N * size)] + sentences[round((k + 1) / N * size):]
        testing_sentences = sentences[round(k / N * size):round((k + 1) / N * size)]
        removed_features = remove_no_appear_features(features, training_sentences)
        train_x, train_y = create_x_y_data(training_sentences, removed_features)
        theta = np.random.rand(len(removed_features) + 1)
        for i in range(EPOCH):
            print('epoch' + str(i), end='\r')
            if i % 500 == 0 or i == EPOCH - 1:
                obj, grad = object_and_grad(train_x, train_y, theta)
                max_update_value = np.max(np.absolute(ETA * grad))
                print('epoch%d:   objective function value %f   max update value %.5e' % (i, obj, max_update_value))
            theta = update_theta(ETA, train_x, train_y, theta)

        test_x, test_y = create_x_y_data(testing_sentences, removed_features)
        predictions = sigmoid(test_x, theta)
        for i in range(1001):
            precision, recall = score_from_variable_threshold(i / 1000, test_y, predictions)
            precision_list[i].append(precision)
            recall_list[i].append(recall)
        print('tested by testing setntences.\n')

    x = [i / 1000 for i in range(1001)]
    precision_y = [sum(e) / N for e in precision_list]
    recall_y = [sum(e) / N for e in recall_list]
    plt.plot(x, precision_y, label='precision')
    plt.plot(x, recall_y, label='recall')
    plt.title('precision and recall')
    plt.xlabel('threshold [-]')
    plt.ylabel('[%]')
    plt.legend()
    fig_path = get_rel_path_from_working_directory(__file__, '../data/fig.png')
    from IPython import embed; embed()
    plt.savefig(fig_path)
    plt.show()
