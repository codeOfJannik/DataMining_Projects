import feedparser
from nltk.corpus import stopwords
import re
from gensim import corpora, models
from itertools import repeat
import numpy as np
import queue

feedlist = ['http://feeds.reuters.com/reuters/topNews',
            'http://feeds.reuters.com/reuters/businessNews',
            'http://feeds.reuters.com/reuters/worldNews',
            'http://feeds2.feedburner.com/time/world',
            'http://feeds2.feedburner.com/time/business',
            'http://feeds2.feedburner.com/time/politics',
            'http://rss.cnn.com/rss/edition.rss',
            'http://rss.cnn.com/rss/edition_world.rss',
            'http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml',
            'http://feeds.nytimes.com/nyt/rss/Business',
            'http://www.nytimes.com/services/xml/rss/nyt/World.xml',
            'http://www.nytimes.com/services/xml/rss/nyt/Economy.xml'
            ]


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


def getWordList(doc):
    words = str.split(doc.lower())
    wordsStripped = [word.strip('().,:;!?-"') for word in words]
    words = [word for word in wordsStripped if 2 < len(word) < 20 and word not in stopwords.words('english')]
    return words


def getarticlewords(feedList):
    allwords = {}
    articlewords = []
    articletitles = []

    for feed in feedlist:
        print('*' * 30)
        print(feed)
        f = feedparser.parse(feed)
        for message in f.entries:
            if re.match(r'\S', message.title):
                print(10 * '-' + message.title + 10 * '-')
                articletitles.append(message.title)
                try:
                    fulltext = stripHTML(message.title + ' ' + message.description)
                except:
                    try:
                        fulltext = stripHTML(message.title + ' ' + message.summary)
                    except:
                        print('no description or summary for', message.title)
                words = getWordList(fulltext)
                docDict = {}
                for word in words:
                    if word in allwords.keys():
                        allwords[word] = allwords[word] + 1
                    else:
                        allwords[word] = 1
                    if word in docDict.keys():
                        docDict[word] = docDict[word] + 1
                    else:
                        docDict[word] = 1
                articlewords.append(docDict)

    nonrelevantwords = [word for word in allwords.keys() if allwords[word] < 4]
    for word in allwords.keys():
        if word not in nonrelevantwords:
            counter = 0
            for a in articlewords:
                if word in a.keys():
                    counter += 1
            if counter / len(articletitles) > 0.3:
                nonrelevantwords.append(word)

    for word in nonrelevantwords:
        catchValue = allwords.pop(word)
        for article in articlewords:
            catchValue = article.pop(word, None)

    for article in articlewords:
        if not article:
            del articletitles[articlewords.index(article)]
            articlewords.remove(article)
        # try without this block
        elif len(article) < 3:
            for word in article.keys():
                allwords[word] -= 1
            articletitles[articlewords.index(article)] = None
            articlewords[articlewords.index(article)] = None

    articlewords = list(filter(None, articlewords))
    articletitles = list(filter(None, articletitles))
    return allwords, articlewords, articletitles


returnValues = getarticlewords(feedlist)
allwords = returnValues[0]
articlewords = returnValues[1]
articletitles = returnValues[2]

print(50 * '*')
for docDict in articlewords:
    print(docDict)


def makematrix(allwords, articlewords):
    dictionary = corpora.Dictionary([allwords.keys()])
    corpus = []
    for doc in articlewords:
        wordList = []
        for k, v in doc.items():
            wordList += [k] * v
        corpus += [dictionary.doc2bow(wordList)]
    matrix = np.zeros(shape=(len(articlewords), len(allwords.keys())))
    for i in range(len(corpus)):
        for tuple in corpus[i]:
            matrix[i][tuple[0]] = tuple[1]
    return matrix


matrix = makematrix(allwords, articlewords)


def cost(A, B):
    result = 0
    if A.shape == B.shape:
        rows = A.shape[0]
        cols = A.shape[1]
        i = 0
        while i < rows:
            j = 0
            while j < cols:
                result += (A[i][j] - B[i][j]) ** 2
                j += 1
            i += 1
        return result
    else:
        print("Error: matrices have different shapes")
        return 0


def nnmf(A, m, it):
    iterations = it
    rows, cols = A.shape
    if m >= cols:
        print("No valid number of features. Must be less than columns.")
        return
    H = np.random.rand(m, cols)
    W = np.random.rand(rows, m)
    costQueue = queue.Queue()
    while it > 0:
        B = np.dot(W, H)
        costs = cost(A, B)
        costQueue.put(costs)
        if it <= iterations - 10:
            if costQueue.get() - costs < 2:
                return H, W
        temp1 = np.array(np.dot(W.transpose(), A))
        temp2 = np.array(np.dot(np.dot(W.transpose(), W), H))
        H = np.array(H * np.true_divide(temp1, temp2))
        W = np.array(W * np.true_divide(np.array(np.dot(A, H.transpose())), np.array(np.dot(np.dot(W, H), H.transpose()))))
        it -= 1
    return H, W


H, W = nnmf(matrix, 20, 200)


def showfeatures(H, W, articletitles, wordvec):
    featurelist = []
    for row in H:
        innerList = []
        index = 0
        for index in range(len(wordvec)):
            innerList.append((row[index], wordvec[index]))
        innerList.sort(key=lambda tup: tup[0], reverse=True)
        featurelist.append(innerList)
    featurelist = [element[:6] for element in featurelist]

    articlefeatures = []
    for row in W:
        innerList = []
        index = 0
        for index in range(len(featurelist)):
            innerList.append((row[index], index))
        innerList.sort(key=lambda tup: tup[0], reverse=True)
        articlefeatures.append(innerList)
    articlefeatures = [element[:2] for element in articlefeatures]

    for index in range(len(articletitles)):
        print(articletitles[index], articlefeatures[index])
        print('-----------', [x[1] for x in featurelist[articlefeatures[index][0][1]]])
        print('-----------', [x[1] for x in featurelist[articlefeatures[index][1][1]]])
        print(30*'*')



showfeatures(H, W, articletitles, list(allwords.keys()))
