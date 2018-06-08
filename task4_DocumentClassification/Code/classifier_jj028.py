import re


minWords = 3
maxWords = 20

# split a text string into its singles words (words must be greater or equal 3 characters and smaller or euqual than 20 characters)
def getwords(doc):
    dictionary = {}
    for word in doc.lower().split():
        word = word.strip('().,:;!?-"\'')
        if len(word) >= minWords or len(word) <= maxWords:
            dictionary[word] = 1
    return dictionary



class Classifier:

    # constructor to initialize the fc and cc dictionaries and the getfeatures instance variable
    def __init__(self, getwords):
        self.fc = {}
        self.cc = {}
        self.initProb = 0.5
        self.getfeatures = getwords

    # method to set the fc counter
    def incf(self, f, cat):
        # when dictionary fc has no word f, create f with an initial value of 0
        #if(not self.fc.has_key(f)):
        if f not in self.fc:
            self.fc[f] = {cat: 0}
        # when word f has no category cat, create cat with an initial value of 0
        #if not self.fc[f].has_key(cat):
        if cat not in self.fc:
            self.fc[f][cat] = 0
        # add 1 as value for category cat for corresponding word f (= key)
        self.fc[f][cat] += 1

    # method to set the cc counter
    def incc(self, cat):
        # when dictionary cc has no category cat, create cat with an initial value of 0
        #if not self.cc.has_key(cat):
        if cat not in self.cc:
            self.cc[cat] = 0
        # add 1 as value for category cat
        self.cc[cat] += 1

    # method to count the occurance of word f in documents of category cat
    def fcount(self, f, cat):
        # check if word f is in dictionary fc
        #if self.fc.has_key(f):
        if f in self.fc:
            # check if word f hast category cat
            #if self.fc[f].has_key(cat):
            if cat in self.fc:
                return self.fc[f][cat]
            else:
                return 0
        else:
            return 0

    # method to count document with category cat
    def catcount(self, cat):
        ##if self.cc.has_key(cat):
        if cat in self.cc:
            return self.cc[cat]
        else:
            return 0

    # method to count all documents
    def totalcount(self):
        tcount = 0
        # add documents for each category cat to counter tcount
        for cat in self.iterkeys():
            tcount += self.cc[cat]
        return tcount

    # split item and count words / documents
    def train(self, item, cat):
        # load all single words of document item into the dictionary words
        words = self.getfeatures(item)

        # add 1 for each word in words to category cat in dictionary fc
        for w in words:
            self.incf(w, cat)
        # add 1 for category cat in dictionary cc
        self.incc(cat)

    # caclulate propability of word f in documents of category cat
    def fprob(self, f, cat):
        # divide count of documents in category cat which contain word f by count of documents in category cat
        #prob = float(self.fcount(f, cat))/float(self.catcount(cat))
        if self.fc[f].get(cat, 0) == 0:
            return 0
        return (float(self.fc[f][cat]) / float(self.cc[cat]))


    # caclulate weighted propability of word f in documents of category cat (with initial propability value)
    def weightedprob(self, f, cat, initProb):
        # initialize count of occurence of word f in training data
        count = 0

        # count occurence of word f in categories of documents
        for category in self.cc.iterkeys():
            c = self.fcount(f, category)
        count += c

        # calculate the weighted propability
        wprob = float(initProb + (count * self.fprob(f, cat))) / float(1 + count)

        return wprob


    # calculate a-posteriori propability for document item for categories cat
    #def prob(self,item,cat):

    #tbd.


# instantiate an object of the classifier class
c = Classifier(getwords)


# train examples from nlp script
c.train("nobody owns the water", "good")
c.train("the quick rabbit jumps fences", "good")
c.train("buy pharmaceuticals now", "bad")
c.train("make quick money at the online casino", "bad")
c.train("the quick brown fox jumps", "good")
c.train("next meeting is at night", "good")
c.train("meeting with your superstar", "bad")
c.train("money like water", "bad")


print (c.prob("the money jumps", "Good"))
print (c.prob("the money jumps", "Bad"))