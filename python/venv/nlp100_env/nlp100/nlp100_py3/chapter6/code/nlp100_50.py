"""
50. 文区切り
(. or ; or : or ? or !) → 空白文字 → 英大文字というパターンを文の区切りと見なし，入力された文書を1行1文の形式で出力せよ．
"""

from mymodule.path_helpers import get_rel_path_from_working_directory
import sys
import re

def devide_text_into_sentences(text):
    """
    文章を文に分ける。
    Args:
        text(str): 文章
    Returns
        sentences(list of str): 文のリスト
    """
    pattern = r'([.:;?!])\s+([A-Z])'
    splited_text = re.split(pattern, text)
    splited_text.insert(0, '')
    it = iter(splited_text)
    sentences = [''.join([x, y, z]) for x, y, z in zip(it, it, it)]
    return sentences

if __name__ == '__main__':
    source_file = get_rel_path_from_working_directory(__file__, '../data/nlp.txt')
    with open(source_file) as f:
        text = f.read()
    sentences = devide_text_into_sentences(text)
    for s in sentences:
        print(s)
