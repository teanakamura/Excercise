"""
52. ステミング
51の出力を入力として受け取り，Porterのステミングアルゴリズムを適用し，単語と語幹をタブ区切り形式で出力せよ． Pythonでは，Porterのステミングアルゴリズムの実装としてstemmingモジュールを利用するとよい．
"""
from mymodule.path_helpers import get_rel_path_from_working_directory
import sys
import re
import nlp100_51

def stemming(words_list):
    """
    Args:
        words_list(list of list of str):
    Returns:
        stemmed_words_list(list of dict of str):
    """
    from stemming.porter2 import stem
    words_and_stems_list = [[[w, stem(re.sub(r'\W$', '', w))] if w else [w] for w in s] for s in words_list]
    return words_and_stems_list

def devide_text_into_words_and_stems(text):
    """
    Args:
        text(str):
    Returns:
        words_and_stems_list(list of list of list of str and str):
    """
    words_list = nlp100_51.devide_text_into_words(text)
    words_and_stems_list = stemming(words_list)
    return words_and_stems_list

if __name__ == '__main__':
    source_file = get_rel_path_from_working_directory(__file__, '../data/nlp.txt')
    with open(source_file) as f:
        text = f.read()
    words_and_stems_list = devide_text_into_words_and_stems(text)
    for sentence in words_and_stems_list:
        for word_and_stem in sentence:
            print(word_and_stem[0] + '\t' + word_and_stem[1] if len(word_and_stem) == 2 else word_and_stem[0])
