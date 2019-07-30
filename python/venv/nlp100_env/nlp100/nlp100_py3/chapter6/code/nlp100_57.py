"""
57. 係り受け解析
Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pdを使うとよい．
"""

import xml.etree.ElementTree as ET
from IPython import embed
import pydot_ng as pd

from mymodule.path_helpers import get_rel_path_from_working_directory
# from mymodule.pycolor import Pycolor
from nlp100_53 import get_parsed_xml_from_rel_path

# def convert_xml_into_dot:
#     pass
# def convert_dot_into_graph:
#     pass
def convert_xml_into_png(xml, *, output='graph', format='png', slice=slice(0, None)):
    root = ET.fromstring(xml)
    for sentence in root.findall('./document/sentences/sentence')[slice]:
        convert_xml_sentence_into_png(sentence, output=output, format=format)

def convert_xml_sentence_into_png(xml_sentence, *, output='graph', format='png'):
    sentence_id = int(xml_sentence.get('id'))
    g = pd.Dot(graph_type='digraph', rankdir='BT', splines='false', margin='0', fontsize='9.5', layout='dot')
    for token in xml_sentence.findall('tokens/token'):
        idx = token.get('id')
        word = token.find('word').text
        n = pd.Node(idx, label='"%s"' % word) # label="," はなぜかerrorで、'","'だと通る。
        g.add_node(n)
    for dep in xml_sentence.findall('dependencies[@type="collapsed-dependencies"]/dep'):
        dep_type = dep.get('type')
        dn = dep.find('governor').get('idx')
        gn = dep.find('dependent').get('idx')
        e = pd.Edge(gn, dn, label='"%s"' % dep_type) # label="," はなぜかerrorで、'","'だと通る。
        g.add_edge(e)
    if output in ['graph', 'both']:
        graph_path = get_rel_path_from_working_directory(__file__, '../data/graph57/sentence_%s.png' % sentence_id)
        print('creating graph of sentence%s' % sentence_id)
        g.write_png(graph_path)
    if output in ['dot', 'both']:
        dot_path = get_rel_path_from_working_directory(__file__, '../data/dot57/sentence_%s.dot' % sentence_id)
        print('creating dot file of sentence%s' % sentence_id)
        with open(dot_path, 'w') as f:
            f.write(g.to_string())

if __name__ == '__main__':
    xml = get_parsed_xml_from_rel_path('../data/nlp')
    convert_xml_into_png(xml, output='both', slice=slice(0, 10))
