"""
56. 共参照解析
Stanford Core NLPの共参照解析の結果に基づき，文中の参照表現（mention）を代表参照表現（representative mention）に置換せよ．ただし，置換するときは，「[代表参照表現](参照表現)」のように，元の参照表現が分かるように配慮せよ．
"""

import xml.etree.ElementTree as ET
import re
# import bigstack

from mymodule.pycolor import Pycolor
from nlp100_53 import get_parsed_xml_from_rel_path

# ところどころうまくいかない
# def _replace_mention_str(xml, represent_color = 'red', non_represent_color = 'yellow', head_color = 'bold'):
#     root = ET.fromstring(xml)
#     rep_color = getattr(Pycolor, represent_color.upper())
#     non_rep_color = getattr(Pycolor, non_represent_color.upper())
#     head_color = getattr(Pycolor, head_color.upper())
#     END = Pycolor.END
#
#     for coreference in root.findall('./document/coreference/coreference'):
#
#         # representative mentionを特定して、xmlを編集するとともにrep_strを獲得する。
#         # representativeなmentionが先頭にあるかはわからないので真っ先にrepresentativeなmentionの処理をする。
#         rep_men = coreference.find('mention[@representative]')
#         # rep_str = rep_men.find('text').text  # 整形されていない文字列が取得できる。
#         rep_str = ''
#         rep_sen = root.find('./document/sentences/sentence[@id="%s"]' % rep_men.find('sentence').text)
#         start_num = int(rep_men.find('start').text)
#         end_num = int(rep_men.find('end').text)
#         head_num = int(rep_men.find('head').text)
#         for i in range(start_num, end_num):
#             token = rep_sen.find('tokens/token[@id="%s"]' % i)
#             org_word = token.find('word').text
#             word = org_word if i != head_num else head_color + org_word + END + non_rep_color
#             # head, start, endは排反ではないので注意。elifは使わない。
#             if i == start_num:
#                 token.set('core_start', 'rep')
#                 token.set('coreference', 'true')
#             if i == end_num - 1:
#                 token.set('core_end', 'rep')
#                 token.set('coreference', 'true')
#             if i == head_num:
#                 token.set('core_head', 'rep')
#                 token.set('coreference', 'true')
#             if re.match(r'\w', org_word):
#                 word = ' ' + word
#             rep_str += word
#         rep_str = rep_str.lstrip(' ')
#
#         # それぞれのmentionごとにxmlを編集する。
#         for mention in coreference.findall('mention'):
#             if mention.get('representative'):
#                 continue
#             sentence = root.find('./document/sentences/sentence[@id="%s"]' % mention.find('sentence').text)
#             start_token = sentence.find('tokens/token[@id="%s"]' % mention.find('start').text)
#             start_token.set('core_start', 'non_rep')
#             start_token.set('coreference', 'true')
#             # start_token.append(ET.Element('represent')); start_token.find('represent').text = rep_str
#             ET.SubElement(start_token, 'represent').text = rep_str
#             head_token = sentence.find('tokens/token[@id="%s"]' % mention.find('head').text)
#             head_token.set('core_head', 'non_rep')
#             head_token.set('coreference', 'true')
#             end_token = sentence.find('tokens/token[@id="%s"]' % (int(mention.find('end').text) - 1))
#             end_token.set('core_end', 'non_rep')
#             end_token.set('coreference', 'true')
#
#     # 整形しながら戻り値を形成。
#     res = ''
#     for token in root.findall('./document/sentences/sentence/tokens/token'):
#         org_word = token.find('word').text
#         word = org_word
#         if token.get('coreference') == 'true':
#             # head -> end, head -> start の順にやる必要あり。
#             if token.get('core_head') == 'rep':
#                 word = head_color + word + END + rep_color
#             elif token.get('core_head') == 'non_rep':
#                 word = head_color + word + END + non_rep_color
#             if token.get('core_end') == 'rep':
#                 word = word + END
#             elif token.get('core_end') == 'non_rep':
#                 word = word + ')' + END
#             if token.get('core_start') == 'rep':
#                 word = rep_color + word
#             elif token.get('core_start') == 'non_rep':
#                 represent = token.find('represent').text
#                 word = non_rep_color + represent + '(' + word
#         if re.match(r'\w', org_word):
#             word = ' ' +  word
#         res += word
#     return res.strip()


def replace_mention_str(xml, *, rep_color='underline', nonrep_color='green', head_color='bold'):
    REP = getattr(Pycolor, rep_color.upper())
    NONREP = getattr(Pycolor, nonrep_color.upper())
    HEAD = getattr(Pycolor, head_color.upper())
    END = Pycolor.END

    def reshape_xml(xml):
        """
        tokensにcoreferenceの情報を追加していく。
        """
        root = ET.fromstring(xml)
        rep_num = 1
        for coreference in root.findall('./document/coreference/coreference'):

            # representative mentionを特定して、xmlを編集するとともにrep_strを獲得する。
            rep_men = coreference.find('mention[@representative]')
            # rep_str = rep_men.find('text').text  # 強調処理されていない文字列が取得できる。
            rep_str = ''
            rep_sen = root.find('./document/sentences/sentence[@id="%s"]' % rep_men.find('sentence').text)
            start_num = int(rep_men.find('start').text)
            end_num = int(rep_men.find('end').text)
            head_num = int(rep_men.find('head').text)
            for i in range(start_num, end_num):
                token = rep_sen.find('tokens/token[@id="%s"]' % i)
                orig_word = token.find('word').text
                word = orig_word if i != head_num else HEAD + orig_word + END
                # head, start, endは排反ではないので注意。elifは使わない。
                if i == start_num:
                    rep_start = token.get('rep_start') or 0
                    token.set('rep_start', rep_start + 1)
                if i == end_num - 1:
                    core_end = token.get('core_end') or 0
                    token.set('core_end', core_end + 1)
                if i == head_num:
                    token.set('core_head', 'rep')
                if re.match(r'\w', orig_word):
                    word = ' ' + word
                rep_str += word
            rep_str = rep_str.lstrip(' ')

            # それぞれのmentionごとにxmlを編集する。
            for mention in coreference.findall('mention'):
                if mention.get('representative'):
                    continue

                sentence = root.find('./document/sentences/sentence[@id="%s"]' % mention.find('sentence').text)

                start_token = sentence.find('tokens/token[@id="%s"]' % mention.find('start').text)
                nonrep_start = start_token.get('nonrep_start') or []
                start_token.set('nonrep_start', nonrep_start + [rep_num])
                # start_token.append(ET.Element('represent')); start_token.find('represent').text = rep_str
                rep = ET.SubElement(start_token, 'rep')
                rep.text = rep_str
                rep.set('rep_num', str(rep_num)) # Stringじゃないと[@rep_num=]で検索できない
                rep_num += 1

                head_token = sentence.find('tokens/token[@id="%s"]' % mention.find('head').text)
                head_token.set('core_head', 'nonrep')

                end_token = sentence.find('tokens/token[@id="%s"]' % (int(mention.find('end').text) - 1))
                core_end = end_token.get('core_end') or 0
                end_token.set('core_end', core_end + 1)
        return root

    def make_mention_expression(token_iter, token=None, *, rep_start=None, nonrep_start=None, core_end=None, story):
        """
        corefernceの情報が追加されたtokensを元にmentionを置き換えたものを形成
        """
        component = ''
        while True:
            if not token:
                try:
                    token = next(token_iter)
                except StopIteration:
                    return component.lstrip(), 0
                rep_start =  token.get('rep_start') or 0
                nonrep_start = token.get('nonrep_start') or []
                core_end = token.get('core_end') or 0
            if nonrep_start:
                rep_num = nonrep_start.pop(0)
                args = {'rep_start': rep_start, 'nonrep_start': nonrep_start, 'core_end': core_end}
                comp, core_end = make_mention_expression(token_iter, token, **args, story=story+1)
                added_color = '' if story == 0 else NONREP
                component += END + ' [%s]' % token.find('rep[@rep_num="%d"]' % rep_num).text \
                                  + NONREP + '(%s)' % comp + END \
                                  + added_color
            elif rep_start: # 再帰関数によって処理するのでここはifではなくelif
                args = {'rep_start': rep_start - 1, 'nonrep_start': nonrep_start, 'core_end': core_end}
                comp, core_end = make_mention_expression(token_iter, token, **args, story=story)
                component += ' ' + REP + comp + END
            else:
                word = token.find('word').text
                if token.get('core_head'):
                    color = locals()[token.get('core_head').upper()]
                    word = HEAD + word + END + color
                pattern = re.compile(r'\w|%s' % re.escape(HEAD))
                if re.match(pattern, word):
                    word = ' ' + word
                component += word
            if core_end:
                return component.lstrip(), core_end - 1
            token = None

    root = reshape_xml(xml)
    token_iter = iter(root.findall('./document/sentences/sentence/tokens/token'))
    res, core_end = make_mention_expression(token_iter, story=0) # story: nonrepの再帰関数の深さ
    return res.strip()

if __name__ == '__main__':
    """
    headを太字にしてみた
    """
    xml = get_parsed_xml_from_rel_path('../data/nlp')
    res = replace_mention_str(xml)
    print(res)


"""解説
### 注意点
+ それぞれのtokenについてrepresentative mentionのstart tokenであること、head tokenであること、end tokenであること、nonrepresentative mentionのstart tokenであること、head tokenであること、end tokenであることは排反ではなく、全て同時に生じうるし、それぞれ最大一つとも限らない。様々な特殊な場合が考えられる。
    + 例
    + representative mentionであり、nonrepresentative mentionである場合。
        + e.g. [rep](nonrep && rep)
    + nonrepresentative mentionで、複数のrepresentative mentionをさす場合。
        + e.g. [rep](... [inner_rep](nonrep) ...)
        + e.g. [rep]([inner_rep](nonrep) ...)

### 解説
+ reshape_xml
    + まずxmlのcoreferenceを順次読み込んでsentencesにcoreference情報を追加していく
    + coreferenceごとにmentionを読み込んでいくが、representative mentionがcoreferenceのtagの先頭にあるかはわからないので、真っ先にrepresentative = 'true' のmentionを読み込んでrepresentative mentionの情報を獲得する。
    + tokenのpropertyとして`rep_start`, `nonrep_start`, `core_head`, `core_end`を追加
        + rep_start (type: int)
            そのtokenがrepresentative mentionのstart tokenであるかを示す。
            複数のrepresentative mentionのstart tokenである場合もあるので、その数を格納する。
        + nonrep_start (type: array of int)
            そのtokenがrepresentative mentionのstart tokenであるかを示す。
            また、対象のrepresentative mentionの情報を`rep`tagとしてtokenに追加する。
            複数のnonrepresentative mentionのstart tokenである場合もあり、`rep`tagと`nonrep_start`propertyとの対応を取るために配列で`rep`tagのid(type: id)を格納する。
        + core_head(type: 'rep' or 'nonrep')
            そのtokenが(non)representative mentionのhead tokenであるかを示す。
            複数の(non)representative mentionのhead tokenである場合もあるが、今回はその情報は利用しないので'rep' or 'nonrep'のいずれかを持つ。
        + core_end(type: int)
            そのtokenが(non)representative mentionのend tokenであるかを示す。
            複数の(non)representative mentionのend tokenである場合もあるので、その数を格納する。
+ make_mention_expression
    + coreference情報を追加したsetntencesから出力文字列を形成していく。
    + 注意点の例にあげたような複雑な場合に対処するために、nonrepresentative mentionの部分の文字列の形成の際は再帰関数を利用した。
    + 再帰関数の代わりにgeneratorで実装してみたい
"""
