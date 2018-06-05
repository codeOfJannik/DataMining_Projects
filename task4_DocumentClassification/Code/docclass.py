# -*- coding: utf-8 -*-

import re

def getwords(doc, mi=3, ma=20):
    #remove unwanted characters
    nonAlpha = re.compile('[^a-zäöüß]')
    doc = nonAlpha.sub(' ', doc.lower())
    #create a dictionary containing each word
    clean = doc.split(' ')
    worddict = {}
    for w in clean:
        if mi <= len(w) <= ma:
            worddict[w] = 1

    return worddict

doc = 'Hallo,du...,daaaaa,drüben'

print getwords(doc)