# -*- coding: utf-8 -*-
import pprint as pp
import numpy as np
import re
from nltk.corpus import stopwords
from collections import Counter
from sklearn.metrics import confusion_matrix, accuracy_score, precision_recall_fscore_support
from IPython.display import display
from nltk.corpus import stopwords
from nltk.stem.snowball import GermanStemmer
import feedparser
import math
import pandas as pd
from gensim import corpora, models
import nltk


feedlist=['http://feeds.reuters.com/reuters/topNews',
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
  p=''
  s=0
  for c in h:
    if c=='<': s=1
    elif c=='>':
      s=0
      p+=' '
    elif s==0: p+=c
  return p

debug = False

def getWordsCounted(doc):
    words = str.split(doc.lower())
    wordsStripped = [word.strip('().,:;!?-"') for word in words]
    words = [word for word in wordsStripped if 2 < len(word) < 20]
    wordDict = dict(Counter(words))
    return wordDict

def getWordList(doc):
    words = str.split(doc.lower())
    wordsStripped = [word.strip('().,:;!?-"') for word in words]
    words = [word for word in wordsStripped if word not in stopwords.words('german')]
    return words

countnews={}
countnews['tech']=0
countnews['nontech']=0
countnews['test']=0
print("--------------------News from trainTech------------------------")
for feed in feedlist:
    print("*"*30)
    print(feed)
    f=feedparser.parse(feed)
    for e in f.entries:
        print('\n---------------------------')
        fulltext=stripHTML(e.title)
        print(fulltext)
        countnews['tech']+=1
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")
print("----------------------------------------------------------------")


def separatewords(text):

    sw = stopwords.words('german')
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 4 and s not in sw]


def getarticlewords():
    allwords = {}
    articlewords = []
    articletitles = []

    # add titles and words
    for key, value in f.items():
        articletitles.append(key)
        words = {}
        for item in separatewords(value):
            # add allwords
            if item in allwords:
                allwords[item] += 1
            else:
                allwords[item] = 1

            # add articlewords
            if item in words:
                words[item] += 1
            else:
                words[item] = 1
        articlewords.append(words)

    return (allwords, articlewords, articletitles)

# Note:
# The wordvec and wordInArt results, will be written as Dict.
# This way no Information about the Words gets lost.
def makematrix(allw, articlew, articletitles):
    temp_articlew = {}
    for index, value in enumerate(articlew):
        temp_articlew[index] = value

    articlew = temp_articlew

    # Declaring Vars
    wordvec = []
    wordInArt = {}

    # Removing words that have a overall Wordcount >= 4
    trimmedV = {}
    for word in allw:
        if allw[word] >= 4:
            trimmedV[word] = allw[word]

    # Removing words that appear > 30% in all Articles
    #
    # artP: Percent per Article occurence
    # percentage: Percentage counting Value
    # trimmedPercent: Copy of trimmedV since Python doesnt allow changing Dicts in a Loop
    artP = (100 / float(len(articlew)))
    percentage = 0
    trimmedPercent = trimmedV.copy()
    for wordV in trimmedV:
        for article in articlew:
            if articlew[article].has_key(wordV):
                percentage += artP
        if percentage > 30:
            trimmedPercent.pop(wordV)
        percentage = 0

    # Create Article/Word Matrix
    #
    # We Loop trough the articlewords for vector i
    # We Loop trough trimmedPercent for vector j
    awMatrix = {}
    valueCount = 0
    popArticleTitles = []
    for article in articlew:
        awMatrix[article] = {}
        valueCount = 0
        for wordAW in trimmedPercent:
            if wordAW in articlew[article]:
                awMatrix[article][wordAW] = articlew[article][wordAW]
                valueCount += 1
            else:
                awMatrix[article][wordAW] = 0

        # Checking if the Article has only 0 values
        # then pop the Artice out of the Dict
        if valueCount == 0:
            awMatrix.pop(article)
            popArticleTitles.append(article)

    # this makes sure that no articles are tried to pop without an existing index
    for index in reversed(popArticleTitles):
        articletitles.pop(index)

    # Writing the wordvec and wordInArt Variables
    # Note: This should give us an reference, so no Additional Space is wasted in RAM
    # nicht tun! wordvec = trimmedPercent
    wordInArt = awMatrix

    # Creating Text File with Matrix
    file = open('../res/awMatrix.txt', 'w')
    wordvecText = ''
    # First Line consists of wordvec
    for i, txtWord in enumerate(trimmedPercent):
        if i != len(trimmedPercent) - 1:
            wordvecText += txtWord + ','
            wordvec.append(txtWord)
        else:
            wordvecText += txtWord + '\n'

    # Creating the Data from wordInArt Matrix
    wordInArtText = ''
    for txtArticle in awMatrix:
        for i, txtData in enumerate(awMatrix[txtArticle]):
            if i != len(awMatrix[txtArticle]) - 1:
                wordInArtText += str(awMatrix[txtArticle][txtData]) + ','
            else:
                wordInArtText += str(awMatrix[txtArticle][txtData]) + '\n'

    # Writing to File
    file.write(wordvecText)
    file.write(wordInArtText)
    file.close()

    return (wordvec, wordInArt, articletitles)


# Returns the Article/Word Matrix as numpy.matrix Object
def transformMatrix(awDict):
    matrixList = []
    # Iterating rough awDict and Converting Data into a nested List
    for row in awDict:
        rowList = []
        if debug:
            print(row)
        for i, col in enumerate(awDict[row]):
            rowList.append(awDict[row][col])
        matrixList.append(rowList)
    # Transforming nested List to an numpy Matrix
    awNumpyMatrix = np.matrix(matrixList)

    return awNumpyMatrix


# A and B are of type numpy.matrix
# returns the summed euclidean distance of the passed matrices
def cost(A, B):
    k = 0
    # create iterators
    iteratorA = A.flat
    iteratorB = B.flat

    try:
        while True:
            # iterate over all elements in both matrices
            Aij = iteratorA.next()
            Bij = iteratorB.next()
            k += pow(Aij - Bij, 2)
            # print "Aij=%d | Bij=%d" % (Aij, Bij)

    except StopIteration:
        pass  # needed because the iterator does not know if there are more elements coming

    return k


# Calculate NNMF
# parameters:
#     A: non-negative Matrix
#     m: count of merkmal
#     it: number of iterations
# returns: {
#     H: Merkmalsmatrix
#     W: Gewichtsmatrix
# }
def nnmf(A, m, it):
    # debug = True
    # get row count and column count of A
    r, c = A.shape

    # step 2:
    ## assert that m < c, else: throw exception
    if m >= c:
        # throw Argument Error
        print "nnmf throws argument Error: m must be smaller than c (count of columns)"
        return

    # step 3+4:
    # initialize matrices H and W
    H = np.matrix(np.random.randint(0, 5, (m, c)))  # 0 needs to be excluded
    W = np.matrix(np.random.randint(0, 5, (r, m)))  # 0 needs to be excluded

    # step 5:
    while it > 0:
        # calculate current product of H and W
        # a)
        B = W * H
        k = cost(A, B)

        if debug:
            pp.pprint({'A': A, 'B': B})
            print "cost: %d" % k

        # break if desired matrix and factorized matrix are very similar
        if k < 5:
            break

        # b) recalculate H
        # Hij = Hij * (W_transposed * A)ij / (W_transposed * W * H)ij
        temp1 = np.array(W.T * A)
        temp2 = np.array(W.T * W * H)
        H = np.matrix(np.array(H) * np.true_divide(temp1, temp2))  # normal divide floors the results
        if debug:
            pp.pprint({'H': H})

        # c) recalculate W
        # Wij = Wij * (A * H_transposed)ij / (W * H * H_transposed)ij
        nextW = np.array(W) * np.true_divide(np.array(A * H.T),
                                             np.array(W * H * H.T))  # normal divide floors the results
        W = np.matrix(nextW)
        if debug:
            pp.pprint({'W': W})

        it -= 1
        if debug:
            print "current values with cost of %.3f: (%d more iterations)" % (k, it)
            pp.pprint({'W': W, 'H': H})
            print "result: cost=%.3f || %d more iterations" % (k, it)
            print "-" * 64

    # return {'H': H, 'W': W}
    return W, H


def showfeatures(W, H, titles, wordvec):
    # Merkmale
    sixImpWords = []
    threeImpArt = []
    rows, columns = H.shape
    for i in range(rows):
        wordlist = []
        sortword = []
        for j in range(len(wordvec)):
            # for j in range(columns) :
            wordlist.append([H[i, j], wordvec[j]])
        sortword = sorted(wordlist, reverse=True)
        sixW = []
        for y in range(6):
            sixW.append(sortword[y][1])
        sixImpWords.append(sixW)

        # Important articles
    rows, columns = W.shape

    for i in range(columns):
        artlist = []
        sortart = []
        for j in range(rows):
            artlist.append([W[j, i], titles[j]])
        sortart = sorted(artlist, reverse=True)

        threArt = []
        for y in range(3):
            threArt.append(sortart[y][1])
        threeImpArt.append(threArt)

    return sixImpWords, threeImpArt