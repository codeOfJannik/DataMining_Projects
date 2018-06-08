from collections import Counter
from sklearn.metrics import confusion_matrix, accuracy_score, precision_recall_fscore_support
from IPython.display import display
from feedparser import parse as ps
import math
import numpy as np
import pandas as pd
from gensim import corpora, models, similarities



def getWordsCounted(doc):
    words = str.split(doc.lower())
    wordsStripped = [word.strip('.,;!?\"\'-_()') for word in words]
    words = [word for word in wordsStripped if 2 < len(word) < 20]
    wordDict = dict(Counter(words))
    return wordDict


def getWordList(doc):
    words = str.split(doc.lower())
    wordsStripped = [word.strip('().,:;!?-"') for word in words]
    words = [word for word in wordsStripped if 2 < len(word) < 20 and word not in stopwords.words('german')]
    GerSt = GermanStemmer("german")
    stemmedWords = [GerSt.stem(word) for word in words]
    return words


def getWordSet(doc):
    return set(getWordList(doc))


class Classifier:
    def __init__(self, getfeatures, cat1, cat2, useTfIdf=False):
        self.fc = {}
        self.cat1 = cat1
        self.cat2 = cat2
        self.cc = {cat1: 0, cat2: 0}
        self.getfeatures = getfeatures
        self.tfidf = useTfIdf
        if useTfIdf:
            self.bowDictcat1 = []
            self.bowDictcat2 = []
            self.dictionary = corpora.Dictionary
            self.bowMatrix = pd.DataFrame
            self.docCount = 0
            self.getfeatures = getWordsCounted

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
            if cat == self.cat1:
                self.bowDictcat1.append(getWordList(item))
            else:
                self.bowDictcat2.append(getWordList(item))

    def fprob(self, f, cat):
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat):
        initprob = 0.5
        if self.tfidf:
            count = self.bowMatrix.loc[self.bowMatrix[f] > 0][f].size
            fprob = np.array(self.bowMatrix.loc[self.bowMatrix['label'] == cat][f]).sum() / self.catcount(cat)
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
        if self.tfidf == True:
            item = self.buildBowMatrix(item)
        for cat in catList:
            probproduct = self.prob(item, cat)
            catprob = self.catcount(cat) / self.totalcount()
            resultDict[probproduct * catprob] = cat
        return resultDict

    def buildBowMatrix(self, item):
        # for k, v in self.bowDict.items():
        #    columns = columns | set(v['words'].keys())
        concat = self.bowDictcat1 + self.bowDictcat2
        self.dictionary = corpora.Dictionary(concat)
        techCorpus = [self.dictionary.doc2bow(doc) for doc in self.bowDictcat1]
        nonTechCorpus = [self.dictionary.doc2bow(doc) for doc in self.bowDictcat2]
        completeCorpus = [self.dictionary.doc2bow(doc) for doc in self.bowDictcat1+self.bowDictcat2]
        labels = []
        [labels.append(self.cat1) for i in range(0, len(techCorpus))]
        [labels.append(self.cat2) for i in range(0, len(nonTechCorpus))]
        tfidf = models.TfidfModel(completeCorpus)
        dataFrame = pd.DataFrame(columns=self.dictionary.token2id.values())
        for i in range(0, len(completeCorpus)):
            corpus_tfidf = tfidf[completeCorpus[i]]
            liste = []
            [liste.append([tup[0], [tup[1]]]) for tup in corpus_tfidf]
            dictDF = pd.DataFrame.from_dict(dict(liste), orient='columns')
            dataFrame = dataFrame.append(dictDF, ignore_index=True)
        dataFrame = dataFrame.fillna(0)
        self.bowMatrix = dataFrame.assign(label=labels)
        itemVec = self.dictionary.doc2bow(getWordList(item))
        return itemVec

    def buildTfIdfMatrix(self, bowMatrix):
        for col in bowMatrix.columns.values:
            if col != 'categoryLabel':
                idf = math.log(self.docCount / bowMatrix.loc[bowMatrix[col] > 0, col].size, 10)
                bowMatrix[col] *= idf
        return bowMatrix

    def prob(self, item, cat):
        itemprobs = []
        if self.tfidf == False:
            for word in self.getfeatures(item):
                itemprobs.append(self.weightedprob(word, cat))
        else:
            for tuple in item:
                prob = self.weightedprob(tuple[0], cat)
                for i in range(0, tuple[1]):
                    itemprobs.append(prob)
        probproduct = 1
        for probability in itemprobs:
            probproduct *= probability
        return probproduct


def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c == '<':
            s = 1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0:
            p += c
    return p


trainTech = [  # not working anymore, using instead one line below:'http://rss.chip.de/c/573/f/7439/index.rss',
    'http://www.chip.de/rss/rss_tests.xml',
    # 'http://feeds.feedburner.com/netzwelt',
    'http://rss1.t-online.de/c/11/53/06/84/11530684.xml',
    'http://www.computerbild.de/rssfeed_2261.xml?node=13',
    'http://www.heise.de/newsticker/heise-top-atom.xml']

trainNonTech = ['http://newsfeed.zeit.de/index',
                'http://newsfeed.zeit.de/wirtschaft/index',
                'http://www.welt.de/politik/?service=Rss',
                'http://www.spiegel.de/schlagzeilen/tops/index.rss',
                'http://www.sueddeutsche.de/app/service/rss/alles/rss.xml',
                'http://www.faz.net/rss/aktuell/'
                ]
test = ["http://rss.golem.de/rss.php?r=sw&feed=RSS0.91",
        'http://newsfeed.zeit.de/politik/index',
        'http://www.welt.de/?service=Rss'
        ]

countnews = {}
countnews['tech'] = 0
countnews['nontech'] = 0
countnews['test'] = 0
print("--------------------News from trainTech------------------------")
for feed in trainTech:
    print("*" * 30)
    print(feed)
    f = ps(feed)
    for e in f.entries:
        print('\n---------------------------')
        try:
            fulltext = stripHTML(e.title + ' ' + e.description)
            print(fulltext)
            countnews['tech'] += 1
        except:
            print("Error while trying to get title or description. Skipped the message.")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")

print("--------------------News from trainNonTech------------------------")
for feed in trainNonTech:
    print("*" * 30)
    print(feed)
    f = ps(feed)
    for e in f.entries:
        print('\n---------------------------')
        try:
            fulltext = stripHTML(e.title + ' ' + e.description)
            print(fulltext)
            countnews['nontech'] += 1
        except:
            print("Error while trying to get title or description. Skipped the message.")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")

print("--------------------News from test------------------------")
for feed in test:
    print("*" * 30)
    print(feed)
    f = ps(feed)
    for e in f.entries:
        print('\n---------------------------')
        try:
            fulltext = stripHTML(e.title + ' ' + e.description)
            print(fulltext)
            countnews['test'] += 1
        except:
            print("Error while trying to get title or description. Skipped the message.")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")

print('Number of used trainings samples in categorie tech', countnews['tech'])
print('Number of used trainings samples in categorie notech', countnews['nontech'])
print('Number of used test samples', countnews['test'])
print('--' * 30)


def trainTheTechClassifier(techClassifier):
    print("--------------------Training with news from trainTech------------------------")
    for feed in trainTech:
        print("*" * 30)
        print(feed)
        f = ps(feed)
        for e in f.entries:
            try:
                fulltext = stripHTML(e.title + ' ' + e.description)
                techClassifier.train(fulltext, 'tech')
            except:
                print('Error while trying to get title or description. Skipped the message.')
    print("------------------------------- done ---------------------------------")

    print("--------------------Training with news from trainNonTech------------------------")
    for feed in trainNonTech:
        print("*" * 30)
        print(feed)
        f = ps(feed)
        for e in f.entries:
            try:
                fulltext = stripHTML(e.title + ' ' + e.description)
                techClassifier.train(fulltext, 'nonTech')
            except:
                print('Error while trying to get title or description. Skipped the message.')
    print("------------------------------- done ---------------------------------")
    return techClassifier


# techClassifier = trainTheTechClassifier(Classifier(getWordList, 'tech', 'nonTech'))


def classifyRSSDocuments(techClassifier):
    resultDF = pd.DataFrame(columns=['label', 'classifierResult'])
    print("--------------------Classify the news from test------------------------")
    feedCount = 0
    for feed in test:
        feedCount += 1
        messageCount = 0
        print("*" * 30)
        print(feed)
        f = ps(feed)
        if feed == 'http://rss.golem.de/rss.php?r=sw&feed=RSS0.91':
            category = 'tech'
        else:
            category = 'nonTech'
        for e in f.entries:
            messageCount += 1
            print('\n---------------------------')
            fulltext = stripHTML(e.title + ' ' + e.description)
            result = techClassifier.classify(fulltext)
            print("the following article is classified as: ", result[sorted(result.keys())[-1]])
            print(fulltext)
            resultDF.loc['feed:' + str(feedCount) + ',message:' + str(messageCount)] = [
                category, result[sorted(result.keys())[-1]]
            ]
    print("----------------------------------------------------------------")
    return resultDF


# resultDF = classifyRSSDocuments(techClassifier)
# display((resultDF,))


def createConfusionMatrixDF(resultDF):
    return pd.DataFrame(index=['tech', 'nonTech'],
                        columns=['tech', 'nonTech'],
                        data=confusion_matrix(resultDF.label, resultDF.classifierResult, labels=['tech', 'nonTech']))


def createPrecisionRecallF1ScoreDF(resultDF):
    precision_recall_Values = precision_recall_fscore_support(resultDF.label,
                                                              resultDF.classifierResult,
                                                              labels=['tech', 'nonTech'])
    precisionRecallDF = pd.DataFrame(columns=['Precision', 'Recall', 'F1-Score'])
    precisionRecallDF.loc['tech'] = [precision_recall_Values[0][0],
                                     precision_recall_Values[1][0],
                                     precision_recall_Values[2][0]]
    precisionRecallDF.loc['nonTech'] = [precision_recall_Values[0][1],
                                        precision_recall_Values[1][1],
                                        precision_recall_Values[2][1]]
    return precisionRecallDF


#display((createConfusionMatrixDF(resultDF),))
#print('Accuracy:', accuracy_score(resultDF.label, resultDF.classifierResult))
#display((createPrecisionRecallF1ScoreDF(resultDF),))

#techClassifier2 = trainTheTechClassifier(Classifier(getWordSet, 'tech', 'nonTech'))
#resultDF2 = classifyRSSDocuments(techClassifier2)

#display((createConfusionMatrixDF(resultDF2),))
#print('Accuracy:', accuracy_score(resultDF2.label, resultDF2.classifierResult))
#display((createPrecisionRecallF1ScoreDF(resultDF2),))

techClassifier3 = trainTheTechClassifier(Classifier(getWordsCounted, 'tech', 'nonTech', useTfIdf=True))
resultDF3 = classifyRSSDocuments(techClassifier3)
display((createConfusionMatrixDF(resultDF3),))
print('Accuracy:', accuracy_score(resultDF3.label, resultDF3.classifierResult))
display((createPrecisionRecallF1ScoreDF(resultDF3),))