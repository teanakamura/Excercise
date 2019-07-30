#!/usr/bin/env python
# -*- coding: utf-8 -*-

def cipher(sentence):
    return "".join(chr(219 - ord(c)) if "a" <= c <= "z" else c for c in sentence)

sentence1 = "anngoubunnhehennkann"
print(cipher(sentence1))
sentence2 = "日本語majirino暗号文"
print(cipher(sentence2))
