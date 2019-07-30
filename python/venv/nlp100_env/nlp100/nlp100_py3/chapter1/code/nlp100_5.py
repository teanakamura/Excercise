 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

def ngram(sentence, char):
    source = sentence if char == 1 else [word.strip(".,") for word in sentence.split()]
    ngram = [source[i:i+2] for i in range(len(source)-1)]
    return ngram

sentence = "I am an NLPer"
print(ngram(sentence, 1))
print(ngram(sentence, 0))
