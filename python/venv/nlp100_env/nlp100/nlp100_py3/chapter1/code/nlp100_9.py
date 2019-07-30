#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import sample
#import random → この時は"sample"ではなく"random.sample"とする。
def typoglycemia(sentence):
    words = sentence.split()
    listed_words = [list(word) for word in words]
    random_words = [list(word[0]) + (sample(word[1:len(word)-1], len(word)-2)) + list(word[len(word)-1]) if len(word) >= 4 else word for word in listed_words]
    random_sentence = " ".join("".join(c for c in word) for word in random_words)
    return random_sentence

from random import shuffle
def typo2(word):
    middle = list(word[1:-1])
    shuffle(middle)
    return word[0]+''.join(middle)+word[-1]
def typo(sentence):
    return ' '.join(typo2(w) if len(w)>4 else w for w in sentence.split())

sentence = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
print(typoglycemia(sentence))
print(typo(sentence))
