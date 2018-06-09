
# split a text string into its singles words (words must be greater or equal 3 characters and smaller or euqual than 20 characters)
def getwords(doc, minWords=3, maxWords=20):
    dictionary = {}
    for word in doc.lower().split():
        word = word.strip('().,:;!?-"\'')
        if len(word) >= minWords and len(word) <= maxWords:
            dictionary[word] = 1
    return dictionary


class Classifier:

    # constructor to initialize the fc and cc dictionaries and the getfeatures instance variable
    def __init__(self, getfeatures):
        self.fc = {}
        self.cc = {}
        self.initprob = 0.5
        self.getfeatures = getfeatures

    # method to set the fc counter
    def incf(self, f, cat):
        # when dictionary fc has no word f, create f with an initial value of 0
        if (f not in self.fc):
            self.fc.update({f: {cat: 0}})
        # when word f has no category cat, create cat with an initial value of 0
        elif (cat not in self.fc[f]):
            self.fc[f].update({cat: 0})
        # add 1 as value for category cat for corresponding word f (= key)
        self.fc[f][cat] += 1

    # method to set the cc counter
    def incc(self, cat):
        # when dictionary cc has no category cat, create cat with an initial value of 0
        if (cat not in self.cc):
            self.cc.update({cat: 0})
        # add 1 as value for category cat
        self.cc[cat] += 1

    # method to count the occurance of word f in documents of category cat
    def fcount(self, f, cat):
        return self.fc[f][cat]

    # method to count document with category cat
    def catcount(self, cat):
        return self.cc[cat]

    # method to count all documents
    def totalcount(self):
        return sum(self.cc.values())

    def fprob(self, f, cat):
        if self.fc[f].get(cat, 0) == 0:
            return 0
        return (float(self.fc[f][cat]) / float(self.cc[cat]))

    # caclulate weighted probability of word f in documents of category cat (with initial probability value)
    def weightedprob(self, f, cat):
        # count occurence of word f in categories of documents
        count = sum(self.fc[f].values())
        wprob_result = self.fprob(f, cat)
        # calculate the weighted probability
        return ((self.initprob + count * wprob_result) / (1 + count))

    # calculate a-posteriori probability for document item for categories cat
    def prob(self, item, cat):
        # divide count of documents in category cat which contain word f by count of documents in category cat
        words = self.getfeatures(item)
        probs = 1
        # calculate the product of the probability of all words in document item
        for w in words:
            probs *= self.weightedprob(w, cat)
        return (probs * (float(self.catcount(cat)) / self.totalcount()))

    # split item and count words / documents
    def train(self, item, cat):
        # load all single words of document item into the dictionary words
        words = self.getfeatures(item)
        # add 1 for each word in words to category cat in dictionary fc
        for word in words:
            self.incf(word, cat)
        # add 1 for category cat in dictionary cc
        self.incc(cat)


# instantiate an object of the classifier class
c = Classifier(getwords)

# dictionary with train examples from nlp script
td = {"the quick rabbit jumps fences": "good",
             "buy pharmaceuticals now": "bad",
             "make quick money at the online casino": "bad",
             "the quick brown fox jumps": "good",
             "next meeting is at night": "good",
             "meeting with your superstar": "bad",
             "money like water": "bad",
             "nobody owns the water": "good"}

# train the train examples
for k, v in list(td.items()):
    c.train(k, v)

# parameters for input / output
given_sentence = "the money jumps"
category1 = "good"
category2 = "bad"

# print probability of a given sentence
print()
print("*****" * 20)
print("The probability that '" + given_sentence + "' belongs to category '" + category1 + "' is: " + str(c.prob(given_sentence, category1)))
print("-----" * 20)
print("The probability that '" + given_sentence + "' belongs to category '" + category2 + "' is: " + str(c.prob(given_sentence, category2)))
print("*****" * 20)
print()
