"""
78. 5分割交差検定
76-77の実験では，学習に用いた事例を評価にも用いたため，正当な評価とは言えない．すなわち，分類器が訓練事例を丸暗記する際の性能を評価しており，モデルの汎化性能を測定していない．そこで，5分割交差検定により，極性分類の正解率，適合率，再現率，F1スコアを求めよ．
"""


from mymodule.path_helpers import get_rel_path_from_working_directory
from random import shuffle
import numpy as np
from stemming.porter2 import stem
from nlp100_73 import update_theta, sigmoid, create_x_y_data, object_and_grad
from nlp100_77 import score


def remove_no_appear_features(features, sentences):
    feature_candidates = np.array([stem(w) for s in sentences for w in s.split()[1:]])
    features = np.array(features)
    removed_features = np.intersect1d(features, feature_candidates)
    print('narraw %d features to %d.' % (len(features), len(removed_features)))
    return removed_features


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
    result = []

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
        result.append(score(test_y, predictions))
        print('tested by testing setntences.\n')

    accuracy = sum((e[0] for e in result)) / N
    precision = sum((e[1] for e in result)) / N
    recall = sum((e[2] for e in result)) / N
    f_value = sum((e[3] for e in result)) / N
    print('accuracy: %f \tprecision: %f \trecall: %f \tFvalue: %f' % (accuracy, precision, recall, f_value))


"""結果
accuracy: 0.750328 	precision: 0.750446 	recall: 0.750421 	Fvalue: 0.750312
"""
