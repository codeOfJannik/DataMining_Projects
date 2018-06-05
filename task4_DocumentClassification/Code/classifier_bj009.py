class Classifier():
    def __init__(self, getfeatures, classes):
        self.fc = {}
        self.classes = classes
        self.cc = self.classDict()
        self.initprob = 0.5

        self.getfeatures = getfeatures

    #creates a base dictionary to be used for each word with the classes
    def classDict(self):
        result = {}
        for cls in self.classes:
            result[cls] = 0

        return result

    #increase the passed feature's counter for the passed category
    def incf(self, f, cat):
        if f not in self.fc:
            self.fc[f] = self.classDict()

        self.fc[f][cat] += 1

    #increase the category counter for the passed category
    def incc(self, cat):
        self.cc[cat] += 1

    #returns the passed feature's counter for the passed category
    def fcount(self, f, cat):
        #get is used because it provides a default if the value does not exist
        return self.fc.get(f, {cat: 0})[cat]

    #returns the counter of the passed category
    def catcount(self, cat):
        return self.cc[cat]

    #returns the sum of all elements
    def totalcount(self):
        return sum(self.cc.itervalues())

    #train a new element and add it to the passed category
    def train(self, item, cat):
        wlist = self.getfeatures(item)
        for w in wlist:
            self.incf(w, cat)
            self.incc(cat)

    #return the probability for the passed feature for the passed category
    def fprob(self, f, cat):
        return ((float)(self.fc.get(f, {cat: 0})[cat]) / self.cc[cat])

    #calculate the weighted probability (avoids 0 for non-exististing words)
    def weightedprob(self, f, cat, initprob=0.5):
        if initprob != 0.5:
            self.initprob = 0.5

        count = 0
        for cls in self.classes:
            count += self.fcount(f, cls)

        return (self.initprob + count * self.fprob(f, cat)) / (1 + count)

    #return the weighteted probability for the passed feature for the passed category
    def prob(self, item, cat):
        product = 1

        for f in self.getfeatures(item):
            product *= self.weightedprob(f, cat)
        return (product * self.cc[cat]) / self.totalcount()

    #return the class the fits the passed item best
    def decide(self, item):
        max_val = -1
        max_cls = ''

        for cls in self.classes:
            prob = self.prob(item, cls)
            if prob > max_val:
                max_val = prob
                max_cls = cls

        return max_cls