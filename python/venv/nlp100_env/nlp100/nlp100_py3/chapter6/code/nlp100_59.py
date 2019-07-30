"""
59. S式の解析
Stanford Core NLPの句構造解析の結果（S式）を読み込み，文中のすべての名詞句（NP）を表示せよ．入れ子になっている名詞句もすべて表示すること．
"""

import xml.etree.ElementTree as ET
from IPython import embed
import pydot_ng as pd
# import re # re moduleは純粋な正規表現を扱うので複数nestされた括弧（nested set）の対応がとれない。
import regex # 再帰マッチが使用できる。

from mymodule.path_helpers import get_rel_path_from_working_directory
from nlp100_53 import get_parsed_xml_from_rel_path

def extract_noun_phrase_from_xml(xml, slice=slice(0, None)):
    root = ET.fromstring(xml)
    for sentence in root.findall('./document/sentences/sentence')[slice]:
        sentence_num = sentence.get('id')
        np_arr = extract_noun_phrase_from_xml_sentence_by_regex(sentence)  # 142ms
        # np_arr = extract_noun_phrase_from_xml_sentence_by_tuple(sentence)  # 96.8ms
        if np_arr:
            print('line%s' % sentence_num)
            for np in np_arr:
                print('\t' + np)

def extract_noun_phrase_from_xml_sentence_by_regex(xml_sentence):
    parse_text = xml_sentence.find('parse').text
    parenthesis_prog = regex.compile(r'''
        (?P<par>  # 以下の正規表現をparとする
            \(
                (?:
                    [^()]  # '(', ')'以外の任意の文字
                    |
                    (?&par)  # parという正規表現を埋め込む
                )+
            \)
        )
    ''', regex.X)
    # parenthesis_prog = regex.compile(r'(?P<par>\((?:[^()]|(?&par))+\))')
    # parenthesis_prog = regex.compile(r'(?>\((?:[^()]|(?R))+\))')  # でもよい
    # parenthesis_prog = regex.compile(r'(\((?:[^()]|(?R))+\))')  # でもよい
    content_prog = regex.compile(r'^[^a-z()]+ ([^()]+)')
    np_arr = []
    def get_content(str):  # 関数内関数じゃない関数にしてnp_arrは引数で渡してやった方が少し速いかもしれない。
        directory_under_content = regex.match(content_prog, str)
        content = [directory_under_content.group(1)] if directory_under_content else []
        for inner_str in regex.findall(parenthesis_prog, str):
            # content.append(get_content(inner_str[1:-1]))
            content.extend(get_content(inner_str[1:-1]))
        if str[:2] == 'NP':
            np_arr.append(' '.join(content))
        return content
    content = get_content(parse_text[1:-1])
    return np_arr

def extract_noun_phrase_from_xml_sentence_by_tuple(xml_sentence):
    parse_text = xml_sentence.find('parse').text
    parse_text = parse_text.translate(str.maketrans({ '(': '("', ')': '")', ' ': '", "' }))
    parse_text = parse_text.replace('"(', '(').replace(')"', ')')
    parse_text = parse_text.rstrip(' ,:"')
    parse_text_tuple = eval(parse_text)
    np_arr = []
    def get_content(obj):
        if type(obj) == str:
            return [obj]
        elif type(obj) == tuple:
            content = []
            for elem in obj[1:]:
                content.extend(get_content(elem))
            if obj[0] == 'NP':
                np_arr.append(' '.join(content))
            return content
    content = get_content(parse_text_tuple)
    return np_arr

# def extract_noun_phrase_from_xml_sentence_by_loop(xml_sentence):

if __name__ == '__main__':
    xml = get_parsed_xml_from_rel_path('../data/nlp')
    embed()
    extract_noun_phrase_from_xml(xml, slice=slice(0, 10))
