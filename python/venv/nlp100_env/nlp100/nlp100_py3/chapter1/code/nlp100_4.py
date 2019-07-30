 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

def atom1(sentence):
    words = sentence.split()
    dict = {}
    for i in range(len(words)):
        if i+1 in [1, 5, 6, 7, 8, 9, 15, 16, 19]:
            dict[words[i][:1]] = i+1
        else:
            dict[words[i][:2]] = i+1
    return dict

def atom2(sentence):
    words = sentence.split()
    dict = {}
    for i,v in enumerate(words,1):
        length=1 if i in [1,5,6,7,8,9,15,16,19] else 2
        dict.update({v[:length]:i})
    return dict

def atom3(sentence):
    return {w[:2-(i in (1,5,6,7,8,9,15,16,19))]:i for i,w in enumerate(sentence.split(),1)}


sentence = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."

print(atom1(sentence))
print(atom2(sentence))
print(atom3(sentence))
