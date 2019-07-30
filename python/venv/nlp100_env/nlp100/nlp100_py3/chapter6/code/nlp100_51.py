"""
51. 単語の切り出し
空白を単語の区切りとみなし，50の出力を入力として受け取り，1行1単語の形式で出力せよ．ただし，文の終端では空行を出力せよ．
"""

from mymodule.path_helpers import get_rel_path_from_working_directory
import sys
import re
import nlp100_50

def devide_sentences_into_words(sentences):
    """
    Args:
        sentences(list of str):
    Returns:
        words_list(list of list of str):
    """
    words_list = [[w for w in s.split()] + [''] for s in sentences]
    # words_list = [[w + '\n' for w in s.split()] + ['\n'] for s in sentences]
    return words_list

def devide_text_into_words(text):
    """
    Args:
        text(str):
    Returns:
        words_list(list of list of str):
    """
    sentences = nlp100_50.devide_text_into_sentences(text)
    words_list = devide_sentences_into_words(sentences)
    return words_list

if __name__ == '__main__':
    source_file = get_rel_path_from_working_directory(__file__, '../data/nlp.txt')
    with open(source_file) as f:
        text = f.read()
    words_list = devide_text_into_words(text)
    for words in words_list:
        for word in words:
            print(word)
