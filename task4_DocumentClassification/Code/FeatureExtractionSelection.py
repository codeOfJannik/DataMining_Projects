from collections import Counter
import numpy as np
import pandas as pd
import math


def getWordsCounted(doc):
    words = str.split(doc.lower())
    wordsStripped = [word.strip('.,!?\"\'-_(') for word in words]
    words = [word for word in wordsStripped if 2 < len(word) < 20]
    wordDict = dict(Counter(words))
    return wordDict


def getWordList(doc):
    words = str.split(doc.lower())
    wordsStripped = [word.strip('.,!?\"\'-_(') for word in words]
    words = [word for word in wordsStripped if 2 < len(word) < 20]
    return words


inputString = "Implementieren Sie eine Funktion getwords(doc), der ein beliebiges Dokument in Form einer " \
              "String-Variablen übergeben wird. In der Funktion soll der String in seine Wörter zerlegt und jedes " \
              "Wort in lowercase transformiert werden. Wörter, die weniger als eine untere Grenze von Zeichen (z.B. " \
              "3) oder mehr als eine obere Grenze von Zeichen (z.B. 20) enthalten, sollen ignoriert werden. Die " \
              "Funktion soll ein dictionary zurückgeben, dessen Keys die Wörter sind. Die Values sollen für jedes " \
              "Wort zunächst auf  1 gesetzt werden. "
print(getWordsCounted(inputString))


class Classifier:
    def __init__(self, getfeatures, cat1, cat2, useTfIdf=False):
        self.fc = {}
        self.cat1 = cat1
        self.cat2 = cat2
        self.cc = {cat1: 0, cat2: 0}
        self.getfeatures = getfeatures
        self.tfidf = useTfIdf
        if useTfIdf:
            self.bowDict = {}
            self.bowMatrix = pd.DataFrame
            self.docCount = 0

    def incf(self, f, cat):
        if f not in list(self.fc.keys()):
            self.fc[f] = {self.cat1: 0, self.cat2: 0}
        self.fc[f][cat] += 1

    def incc(self, cat):
        self.cc[cat] += 1

    def fcount(self, f, cat):
        return self.fc[f][cat]

    def catcount(self, cat):
        return self.cc[cat]

    def totalcount(self):
        catcounts = np.array(list(self.cc.values()))
        return catcounts.sum()

    def train(self, item, cat):
        self.incc(cat)
        if self.tfidf == False:
            wordList = self.getfeatures(item)
            [self.incf(word, cat) for word in wordList]
        else:
            self.docCount += 1
            wordDict = self.getfeatures(item)
            docDict = {'cat': cat, 'words': wordDict}
            self.bowDict['doc' + str(self.docCount)] = docDict

    def fprob(self, f, cat):
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat):
        initprob = 0.5
        if self.tfidf:
            count = self.bowMatrix.loc[self.bowMatrix[f] > 0][f].size
            fprob = np.array(self.bowMatrix.loc[self.bowMatrix['categoryLabel'] == cat][f]).sum() / self.catcount(cat)
        else:
            if f in self.fc.keys():
                values = list(self.fc[f].values())
                count = np.array(values).sum()
                fprob = self.fprob(f, cat)
            else:
                count = 0
                fprob = 0
        return (initprob + count * fprob) / (1 + count)

    def classify(self, item):
        catList = list(self.cc.keys())
        resultDict = {}
        if self.tfidf == False:
            for cat in catList:
                probproduct = self.prob(item, cat)
                catprob = self.catcount(cat) / self.totalcount()
                resultDict[probproduct * catprob] = cat
        else:
            self.bowMatrix = self.buildBowMatrix()
            self.bowMatrix = self.buildTfIdfMatrix(self.bowMatrix)
            for cat in catList:
                probproduct = self.prob(item, cat)
                catprob = self.catcount(cat) / self.totalcount()
                resultDict[probproduct * catprob] = cat
        return resultDict

    def buildBowMatrix(self):
        columns = set()
        for k, v in self.bowDict.items():
            columns = columns | set(v['words'].keys())
        columnList = list(columns)
        columnList.append('categoryLabel')
        bowMatrix = pd.DataFrame(columns=columnList)
        for k, v in self.bowDict.items():
            docValues = []
            wordList = v['words'].keys()
            for word in columns:
                if word in wordList and word != 'categoryLabel':
                    docValues.append(v['words'][word])
                elif word != 'categoryLabel':
                    docValues.append(0)
                else:
                    pass
            docValues.append(v['cat'])
            bowMatrix.loc[k] = docValues
        return bowMatrix

    def buildTfIdfMatrix(self, bowMatrix):
        for col in bowMatrix.columns.values:
            if col != 'categoryLabel':
                idf = math.log(self.docCount / bowMatrix.loc[bowMatrix[col] > 0, col].size, 10)
                bowMatrix[col] *= idf
        return bowMatrix

    def prob(self, item, cat):
        itemprobs = []
        for word in self.getfeatures(item):
            itemprobs.append(self.weightedprob(word, cat))
        probproduct = 1
        for probability in itemprobs:
            probproduct *= probability
        return probproduct


classifier = Classifier(getWordsCounted, 'good', 'bad', useTfIdf=True)

trainData = {'the quick rabbit jumps fences': 'good', 'buy pharmaceuticals now': 'bad',
             'make quick money at the online casino': 'bad', 'the quick brown fox jumps': 'good',
             'next meeting is at night': 'good', 'meeting with your superstar': 'bad', 'money like water': 'bad',
             'nobody owns the water': 'good'}

for key, value in trainData.items():
    classifier.train(key, value)

print(classifier.classify("the money jumps"))
