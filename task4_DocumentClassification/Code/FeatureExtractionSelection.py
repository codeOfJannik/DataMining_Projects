from collections import Counter
import numpy as np


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
    def __init__(self):
        self.fc = {}
        self.cc = {'good': 0, 'bad': 0}

    def incf(self, f, cat):
        if f not in self.fc.keys():
            self.fc[f] = {'good': 0, 'bad': 0}
        self.fc[f][cat] += 1

    def getfeatures(self, item):
        return getWordList(item)

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
        wordList = self.getfeatures(item)
        [self.incf(word, cat) for word in wordList]

    def fprob(self, f, cat):
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat):
        initprob = 0.5
        values = list(self.fc[f].values())
        count = np.array(values).sum()
        return (initprob + count * self.fprob(f, cat)) / (1 + count)

    def classify(self, item):
        catList = self.cc.keys()
        resultDict = {}
        for cat in catList:
            probproduct = self.prob(item, cat)
            catprob = self.catcount(cat) / self.totalcount()
            resultDict[probproduct * catprob] = cat
        return resultDict

    def prob(self, item, cat):
        itemprobs = []
        for word in self.getfeatures(item):
            itemprobs.append(self.weightedprob(word, cat))
        probproduct = 1
        for probability in itemprobs:
            probproduct *= probability
        return probproduct


classifier = Classifier()

trainData = {'the quick rabbit jumps fences': 'good', 'buy pharmaceuticals now': 'bad',
             'make quick money at the online casino': 'bad', 'the quick brown fox jumps': 'good',
             'next meeting is at night': 'good', 'meeting with your superstar': 'bad', 'money like water': 'bad',
             'nobody owns the water': 'good'}

for key, value in trainData.items():
    classifier.train(key, value)

print(classifier.classify("the money jumps"))
