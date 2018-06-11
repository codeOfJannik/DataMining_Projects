import feedparser
from nltk.corpus import stopwords
import re

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
        allwords.pop(word)
        for article in articlewords:
            article.pop(word, None)

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

[print(key,':', value) for key, value in allwords.items()]
print(50*'*')
[print(docDict) for docDict in articlewords]