 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

def ngram(sentence):
    ngram = [sentence[i:i+2] for i in range(len(sentence)-1)]
    return ngram

def group(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    print(set1|set2)
    print(set1&set2)
    print(set1-set2)

def search(list, bigram):
    return bigram in list

sentence1 = "paraparaparadise"
sentence2 = "paragraph"

list1 = ngram(sentence1)
list2 = ngram(sentence2)
group(list1, list2)
print(search(list1, "se"))
print(search(list2, "se"))
