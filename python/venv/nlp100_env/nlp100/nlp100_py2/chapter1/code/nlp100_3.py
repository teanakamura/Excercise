#!/usr/bin/env python
# -*- coding: utf-8 -*-

def split_in_words1(text):
    return [len(word) for word in text.replace(","," ").replace("."," ").split()]

# Python3系
# def split_in_words2(text):
#     dic = str.maketrans(',.', '  ')
#     return [len(word) for word in text.trancelate(dic).split()]

def split_in_words3(text):
    return [len(word.strip(".,")) for word in text.split()]

text = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
print(split_in_words1(text))
print(split_in_words3(text))
