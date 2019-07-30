from IPython import embed

import spacy
import MeCab
import numpy as np
import sklearn.preprocessing as sp
from collections import Counter

voc_size = 100

doc_arr = []
counter = Counter()
nlp = spacy.load('en_core_web_sm')
with open('./data/GlobalVoices/raw/GlobalVoices.en-jp.en') as e:
    for i, l in enumerate(e, 1):
        print(f'english: {i}', end='\r')
        doc = nlp(l.strip())
        snt_arr = [token.lower_ for token in doc]
        counter.update(snt_arr)
        snt_arr.append('<EOS>')
        snt_arr = ['<BOS>'] + snt_arr
        doc_arr.append(snt_arr)
        if i == 300: break #####################
    print()
en_voc = [k for k, v in counter.most_common(voc_size)]
rep_doc_arr = [[w if w in en_voc else '<UNK>' for w in l] for l in doc_arr]
en_voc.append('<UNK>')
en_le = sp.LabelEncoder()
en_le.fit(en_voc)
en_txt_id = np.array([[en_le.transform(l)] for l in rep_doc_arr])
# int_encoded = int_encoded.reshape(len(int_encoded), 1)
# ohe = sp.OneHotEncoder()
# en_oh_encoded = ohe.transform(int_encoded)

doc_arr = []
counter.clear()
tagger = MeCab.Tagger("-Owakati")
with open('./data/GlobalVoices/raw/GlobalVoices.en-jp.jp') as j:
    for i, l in enumerate(j, 1):
        print(f'japanese: {i}', end='\r')
        # doc_gen = tagger.parseToNode(l) # doc_gen.next, doc_gen.surface
        doc = tagger.parse(l).split()
        snt_arr = [token for token in snt_arr if not token == '']
        counter.update(snt_arr[1:])
        snt_arr.append('<EOS>')
        snt_arr[0] = '<BOS>'
        doc_arr.append(snt_arr)
        if i == 300: break ##############################
    print()
ja_voc = [k for k, v in counter.most_common(voc_size)]
rep_doc_arr = [[w if w in ja_voc else '<UNK>' for w in l] for l in doc_arr]
ja_voc.append('<UNK>')
ja_le = sp.LabelEncoder()
ja_le.fit(ja_voc)
ja_txt_id = np.array([[ja_le.transform(l)] for l in rep_doc_arr])
# int_encoded = int_encoded.reshape(len(int_encoded), 1)
# ohe = sp.OneHotEncoder()
# ja_oh_encoded = ohe.transform(int_encoded)

np.save('./data/en_classes.npy', en_le.classes_)
np.save('./data/ja_classes.npy', ja_le.classes_)
np.save('./data/en_txt_id.npy', en_txt_id)
np.save('./data/ja_txt_id.npy', ja_txt_id)
