from classifier_bj009 import Classifier
from docclass import getwords
from parseTechFeed import trainNonTech,stripHTML,countnews,trainTech,test
import feedparser
import pprint as pp
import pickle as pickle

test_news = {'tech': [], 'nontech': []}

classifier = Classifier(getwords, ['tech', 'nontech'])
classifier.initprob = 0.5

for feed in trainTech:
    f = feedparser.parse(feed)
    for e in f.entries:
        fulltext = stripHTML(e.title + ' ' + e.description)
        countnews['tech'] += 1
        classifier.train(fulltext, 'tech')

for feed in trainNonTech:
    f = feedparser.parse(feed)
    for e in f.entries:
        fulltext = stripHTML(e.title + ' ' + e.description)
        countnews['nontech'] += 1
        classifier.train(fulltext, 'nontech')

for feed in test:
    f = feedparser.parse(feed)
    for e in f.entries:
        fulltext = stripHTML(e.title + ' ' + e.description)
        countnews['test'] += 1
        classification = classifier.decide(fulltext)
        test_news[classification].append([fulltext,
            classifier.prob(fulltext, 'tech'),
            classifier.prob(fulltext, 'nontech')]
        )

