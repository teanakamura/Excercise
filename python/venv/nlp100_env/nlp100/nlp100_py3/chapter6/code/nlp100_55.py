"""
55. 固有表現抽出
入力文中の人名をすべて抜き出せ．
"""

import xml.etree.ElementTree as ET

from nlp100_53 import get_parsed_xml_from_rel_path

if __name__ == '__main__':
    xml = get_parsed_xml_from_rel_path('../data/nlp')
    root = ET.fromstring(xml)
    person_arr = [
        token.find('word').text
            for token in root.findall('./document/sentences/sentence/tokens/token')
            if token.find('NER').text == 'PERSON'
    ]
    print('\t'.join(person_arr))
