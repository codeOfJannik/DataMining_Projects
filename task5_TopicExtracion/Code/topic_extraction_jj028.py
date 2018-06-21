import feedparser
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import itertools

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


# Parses feed, strip Html and return a list containing titles and descriptions
def get_titles_and_descriptions(feedlist):
    # Contains (title, description)-tuples
    title_desc_list = []
    # Counts number of articles
    article_counter = 0
    # Counts number of articles with missing description
    no_description = 0
    for feed in feedlist:
        parsed = feedparser.parse(feed)

        for e in parsed.entries:
            article_counter += 1
            if 'description' in e:
                title_desc_list.append((stripHTML(e.title), stripHTML(e.description)))
            else:
                no_description += 1

    print()
    print("***" * 20)
    print("Parsed articles: " + str(article_counter))
    print()
    print("Parsed articles witout description: " + str(no_description))
    print("***" * 20)
    print()

    return title_desc_list

    #"Parsed " + str(article_counter) + " articles. " + str(
    #    no_description) + " of them were without a description and are therefore no longer considered."


feeds = get_titles_and_descriptions(feedlist)

print("Content of (title-description)-list \n")
print("[")
for i in range(5):
    print(u"({}, \n\t {})".format(feeds[i][0], feeds[i][1]))

print("...")
print("]")


def getarticlewords(articles, blacklist=[], lowBorder=3, highBorder=20):
    allwords = {}
    articlewords = []
    articletitles = []
    blacklist = [x.lower() for x in blacklist]

    stop_words = set(stopwords.words('english'))

    for article in articles:
        articletitles.append(article[0])

        currentarticlewords = {}
        for word in itertools.chain(article[0].lower().split(), article[1].lower().split()):
            word = word.strip('().,:;!?-"\'')
            if word not in stop_words and word not in blacklist and len(word) >= lowBorder and len(word) <= highBorder:
                if word in allwords.keys():
                    allwords[word] += 1
                else:
                    allwords[word] = 1
                if word in currentarticlewords.keys():
                    currentarticlewords[word] += 1
                else:
                    currentarticlewords[word] = 1
        articlewords.append(currentarticlewords)

    print()
    print("***" * 20)
    print("Different words: " + str(len(allwords)))
    print()
    print("Articles: " + str(len(articletitles)))
    print("***" * 20)
    print()

    return cleanedarticlewords(allwords, articlewords, articletitles)

    #"Result of Analysis (before cleaning): " + str(len(allwords)) + " different words and " + str(
    #   len(articletitles)) + " articles remaining."
    #return cleanarticlewords(allwords, articlewords, articletitles)


def cleanedarticlewords(allwords, articlewords, articletitles):
    articlecount = len(articletitles)
    removewords = []

    #for word, count in allwords.iteritems():
    for word, count in allwords.items():
        # remove words that occurred less than 4 times
        if count < 4:
            removewords.append(word)
            for article in articlewords:
                if word in article.keys():
                    del article[word]
        # remove all words that occur in more than 30% of all documents
        else:
            wordcount = 0
            for article in articlewords:
                if word in article.keys():
                    wordcount += 1
            if wordcount > articlecount * 0.3:
                removewords.append(word)
                for article in articlewords:
                    if word in article.keys():
                        del article[word]

    for word in removewords:
        del allwords[word]

    # remove empty dictionarys
    removedicts = []
    for idx, article in enumerate(articlewords):
        if not article:
            removedicts.append(idx)
    for idx in sorted(removedicts, reverse=True):
        del articlewords[idx]
        del articletitles[idx]

    print()
    print("***" * 20)
    print("Different words (cleaned): " + str(len(allwords)))
    print()
    print("Articles (cleaned): " + str(len(articletitles)))
    print("***" * 20)
    print()

    return allwords, articlewords, articletitles

    #"Result of Analysis (after cleaning): " + str(len(allwords)) + " different words and " + str(
    #    len(articletitles)) + " articles remaining."


word_blacklist = ["reuters"]
(allwords, articlewords, articletitles) = getarticlewords(feeds, blacklist=word_blacklist)

print("\nallwords: ")
print("{")
for i in range(5):
    #print("{:>10}\t : \t{}".format(allwords.keys()[i], allwords.values()[i]))
    #print("{:>10}\t : \t{}".format(allwords()[i], allwords.values()[i]))
    #awk = allwords[list(allwords.keys())[i]]
    awk1 = list(allwords.keys())
    awv1 = list(allwords.values())
    #awv = allwords[list(allwords.values())[i]]

    #print("{:>10}\t : \t{}".format(list(allwords.keys()[i])), allwords.values()[i])
    print("{:>10}\t : \t{}".format(awk1[i], awv1[i]))

print("...")
print("}")

print("\narticlewords")
print("[")
for i in range(5):
    print("{")
    for j in range(2):
        awk2 = list(articlewords[i].keys())
        awv2 = list(articlewords[i].values())
        #print("{:>10}\t : \t{}".format(articlewords[i].keys()[j], articlewords[i].values()[j]))
        #print("{:>10}\t : \t{}".format(articlewords()[j], articlewords[i].values()[j]))
        #print("{:>10}\t : \t{}".format(articlewords[list(articlewords[i].keys()[j])], articlewords[i].values()[j]))
        print("{:>10}\t : \t{}".format(awk2[j], awv2[j]))

    print("...")
    print("}")
    if (i != 5):
        print(",")
print("...")
print("]")

print("\narticletitles")
print("[")
for i in range(5):
    print(articletitles[i])
    if (i != 5):
        print(",")
print("]")