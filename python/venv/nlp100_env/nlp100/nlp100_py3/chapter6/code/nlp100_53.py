"""
53. Tokenization
Stanford Core NLPを用い，入力テキストの解析結果をXML形式で得よ．また，このXMLファイルを読み込み，入力テキストを1行1単語の形式で出力せよ．
"""

from stanfordcorenlp import StanfordCoreNLP
import xml.etree.ElementTree as ET
from pprint import pprint
from IPython import embed

from mymodule import path_helpers, stanford_corenlp

def convert_into_xml(text):
    stanford_corenlp.stanford_corenlp_with_server()
    with StanfordCoreNLP('http://localhost', port=9000) as parser:
    # with stanford_corenlp.StanfordCoreNLP(r'/usr/local/lib/stanford-corenlp-full-2018-10-05/') as nlp: # sudo で実行する必要がある
        props={'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, dcoref', 'pipelineLanguage': 'en', 'outputFormat': 'xml'}
        return parser.annotate(text, properties = props)

def reshape_xml_text(xml):
    root = ET.fromstring(xml)
    parsed_arr = \
    [
        [
            {
                # 'sentence_id': sentence.get('id'),
                # 'token_id': token.get('id'),
                'word': token.find('word').text,
                'lemmma': token.find('lemma').text,
                'COB': token.find('CharacterOffsetBegin').text,  # CharacterOffsetBegin
                'COE': token.find('CharacterOffsetEnd').text,  # CharacterOffsetEnd
                'POS': token.find('POS').text,  # PartOfSpeech
                'NER': token.find('NER').text,  # NamedEntityRecognition
                'Speaker': None if token.find('Speaker') == None else token.find('Speaker').text
            } for token in sentence.find('tokens').iter('token')
        ] for sentence in root.findall('./document/sentences/sentence')
    ]
    return(parsed_arr)

def get_parsed_xml_from_rel_path(path):
    """
    実行ファイルからの相対パスでxmlファイルを読み込む。xmlファイルがない場合は同名のtxtファイルを解析結果として返す（xmlファイルも作る）。
    """
    source_xml_file = path_helpers.get_rel_path_from_working_directory(__file__, path + '.xml')
    try:
        with open(source_xml_file) as f:
            xml_text = f.read()
    except FileNotFoundError:
        source_txt_file = path_helpers.get_rel_path_from_working_directory(__file__, path + '.txt')
        with open(source_txt_file) as source:
            text = source.read()
        xml_text = convert_into_xml(text)
        with open(source_xml_file, 'w') as output:
            output.write(xml_text)
    return(xml_text)

if __name__ == '__main__':
    xml_text = get_parsed_xml_from_rel_path('../data/nlp')
    parsed_arr = reshape_xml_text(xml_text)
    pprint(parsed_arr, depth = 3, width = 1000)
