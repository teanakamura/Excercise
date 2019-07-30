"""
54. 品詞タグ付け
Stanford Core NLPの解析結果XMLを読み込み，単語，レンマ，品詞をタブ区切り形式で出力せよ．
"""

import xml.etree.ElementTree as ET

from nlp100_53 import get_parsed_xml_from_rel_path

if __name__ == '__main__':
    xml = get_parsed_xml_from_rel_path('../data/nlp')
    root = ET.fromstring(xml)
    for sentence in root.findall('./document/sentences/sentence'):
        for token in sentence.find('tokens').iter('token'):
            token_arr = [token.find('word').text, token.find('lemma').text, token.find('POS').text]
            print('\t'.join(token_arr))
        print()
