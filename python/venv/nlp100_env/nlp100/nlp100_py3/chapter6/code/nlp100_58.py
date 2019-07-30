"""
58. タプルの抽出
Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）に基づき，「主語 述語 目的語」の組をタブ区切り形式で出力せよ．ただし，主語，述語，目的語の定義は以下を参考にせよ．
・述語: nsubj関係とdobj関係の子（dependant）を持つ単語
・主語: 述語からnsubj関係にある子（dependent）
・目的語: 述語からdobj関係にある子（dependent）
"""

import xml.etree.ElementTree as ET
from IPython import embed
import pydot_ng as pd

from mymodule.path_helpers import get_rel_path_from_working_directory
# from mymodule.pycolor import Pycolor
from nlp100_53 import get_parsed_xml_from_rel_path

def convert_xml_into_tuple(xml, slice=slice(0, None)):
    root = ET.fromstring(xml)
    for sentence in root.findall('./document/sentences/sentence')[slice]:
        tuple_arr = convert_xml_sentence_into_tuple(sentence)
        if tuple_arr:
            print('line%s' % sentence.get('id'))
            for tuple in tuple_arr:
                print('\t'.join(tuple))


def convert_xml_sentence_into_tuple(xml_sentence):
    nsubj_deps = {
        dep.find('governor').get('idx'): (dep.find('governor').text, dep.find('dependent').text)
            for dep in xml_sentence.findall('dependencies[@type="collapsed-dependencies"]/dep[@type="nsubj"]')
    }
    dobj_deps = {
        dep.find('governor').get('idx'): (dep.find('governor').text, dep.find('dependent').text)
            for dep in xml_sentence.findall('dependencies[@type="collapsed-dependencies"]/dep[@type="dobj"]')
    }
    predicate_verb_keys = nsubj_deps.keys() & dobj_deps.keys()
    return [[nsubj_deps[key][1], nsubj_deps[key][0], dobj_deps[key][1]] for key in predicate_verb_keys]
    # for key in predicate_verb_keys:
    #     return(nsubj_deps[key][1], nsubj_deps[key][0], dobj_deps[key][1])

if __name__ == '__main__':
    xml = get_parsed_xml_from_rel_path('../data/nlp')
    convert_xml_into_tuple(xml, slice=slice(0, 10))
