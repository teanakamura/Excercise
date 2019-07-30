"""
75. 素性の重み
73で学習したロジスティック回帰モデルの中で，重みの高い素性トップ10と，重みの低い素性トップ10を確認せよ．
"""


import numpy as np
from mymodule.path_helpers import get_rel_path_from_working_directory
from IPython import embed

if __name__ == '__main__':
    features_file = get_rel_path_from_working_directory(__file__, '../data/features.txt')
    theta_file = get_rel_path_from_working_directory(__file__, '../data/theta.npy')
    with open(features_file) as f:
        features = f.read().split()
    theta = np.load(theta_file)
    # sorted_features = np.array(features)[np.argsort(np.delete(theta, 0))]
    features_dict = {feature: theta for feature, theta in zip(features, np.delete(theta, 0))}
    sorted_features = sorted(features_dict.items(), key=lambda x: x[1])
    print('worst 10')
    for i in range(10):
        print('%d: %s (%f)' % (i+1, *sorted_features[i]))
    print('top 10')
    for i in range(-1, -11, -1):
        print('%d: %s (%f)' % (-i, *sorted_features[i]))
