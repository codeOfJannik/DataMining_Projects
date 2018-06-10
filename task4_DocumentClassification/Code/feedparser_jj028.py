import feedparser
from classifier_jj028 import Classifier
from classifier_jj028 import getwords


def stripHTML(h):
  p = ''
  s = 0
  for c in h:
    if c == '<': s = 1
    elif c == '>':
      s = 0
      p += ' '
    elif s == 0:
      p += c
  return p


trainTech = ['http://rss.chip.de/c/573/f/7439/index.rss',
            # 'http://feeds.feedburner.com/netzwelt',
            'http://rss1.t-online.de/c/11/53/06/84/11530684.xml',
            'http://www.computerbild.de/rssfeed_2261.xml?node=13',
            'http://www.heise.de/newsticker/heise-top-atom.xml']

trainNonTech = ['http://newsfeed.zeit.de/index',
                'http://newsfeed.zeit.de/wirtschaft/index',
                'http://www.welt.de/politik/?service=Rss',
                'http://www.spiegel.de/schlagzeilen/tops/index.rss',
                'http://www.sueddeutsche.de/app/service/rss/alles/rss.xml',
                'http://www.faz.net/rss/aktuell/']

test = ["http://rss.golem.de/rss.php?r=sw&feed=RSS0.91",
        'http://newsfeed.zeit.de/politik/index',
        'http://www.welt.de/?service=Rss']

countnews = {}
countnews["tech"] = 0
countnews["nontech"] = 0
countnews["test"] = 0


# instantiate an object of the classifier class
c = Classifier(getwords)


print ("--------------------News from trainTech------------------------")
for feed in trainTech:
    print ("*" * 30)
    print (feed)
    f = feedparser.parse(feed)
    for e in f.entries:
        print ('\n---------------------------')
        fulltext = stripHTML(e.title + ' ' + e.description)
        #print (fulltext)
        countnews["tech"] += 1
        # train classifier with news from tech categories
        c.train(fulltext, "tech")

print ("----------------------------------------------------------------")
print ("----------------------------------------------------------------")
print ("----------------------------------------------------------------")

print ("--------------------News from trainNonTech------------------------")
for feed in trainNonTech:
    print ("*" * 30)
    print (feed)
    f = feedparser.parse(feed)
    for e in f.entries:
        print ('\n---------------------------')
        fulltext = stripHTML(e.title + ' ' + e.description)
        #print (fulltext)
        countnews["nontech"] += 1
        # train classifier with news from non-tech categories
        c.train(fulltext, "nontech")

print ("----------------------------------------------------------------")
print ("----------------------------------------------------------------")
print ("----------------------------------------------------------------")

print ("--------------------News from test------------------------")
for feed in test:
    print ("*" * 30)
    print (feed)
    f = feedparser.parse(feed)
    for e in f.entries:
        print ('\n---------------------------')
        fulltext = stripHTML(e.title + ' ' + e.description)
        #print (fulltext)
        countnews["test"] += 1
        # print classification (probability that a given sentence belongs to a certain category)
        print("Klassifikation: " + str(c.classify(fulltext)))

print ("----------------------------------------------------------------")
print ("----------------------------------------------------------------")
print ("----------------------------------------------------------------")

print ('Number of used trainings samples in categorie tech' + str(countnews["tech"]))
print ('Number of used trainings samples in categorie notech' + str(countnews["nontech"]))
print ('Number of used test samples' + str(countnews["test"]))
print ('--' * 30)