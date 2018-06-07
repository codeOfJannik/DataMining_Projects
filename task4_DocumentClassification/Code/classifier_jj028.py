import re


# split a text string into its singles words (words must be greater or equal 3 characters and smaller or euqual than 20 characters)
def getwords(doc):
    dictionary = {}
    for word in doc.split().strip('().,:;!?-"\'').lower():
        if len(word) >= 3 or len(word) <= 20:
            dictionary[word] = 1
    return dictionary



class Classifier:

    # constructor to initialize the fc and cc dictionaries and the getfeatures instance variable
    def __init__(self, getfeatures):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getwords()


    # method to set the fc counter
    def incf(self, f, cat):
        # when dictionary fc has no word f, create f with an initial value of 0
        if not self.fc.has_key(f):
            self.fc[f] = {cat: 0}
        # when word f has no category cat, create cat with an initial value of 0
        if not self.fc[f].has_key(cat):
            self.fc[cat] = 0
        # add 1 as value for category cat for corresponding word f (= key)
        self.fc[f][cat] += 1


    # method to set the cc counter
    def incc(self, cat):
        # when dictionary cc has no category cat, create cat with an initial value of 0
        if not self.cc.has_key(cat):
            self.cc[cat] = 0
        # add 1 as value for category cat
        self.cc[cat] += 1


    # method to count the occurance of word f in documents of category cat
    def fcount(self, f, cat):
        # check if word f is in dictionary fc
        if self.fc.has_key(f):
            #check if word f hast category cat
            if self.fc[f].has_key(cat):
                return self.fc[f][cat]
            else:
                return 0
        else:
            return 0


    # method to count document with category cat
    def catcount(self, cat):
        if self.cc.has_key(cat):
            return self.cc(cat)
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


    #def fprob(self, f, cat):

    #def weightedprob(self, f, cat):

