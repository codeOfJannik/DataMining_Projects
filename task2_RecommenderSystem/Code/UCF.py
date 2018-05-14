from SimilarityOfCritics import critics,topMatches,sim_RusselRao,sim_pearson,sim_euclid

'''
NR.1
#1 weight calcuation
#2 exclude items with negative correlation
#3 remove bought movies
#4 removes and returns last object from the list
#5 relevant similarity values
#6 key is a function that will be called to transform the collections items before they are compared.
   lambda creates an anonymous function. The parameter list and code block are delineated by colon.
'''
def getRecommendations(prefs,person,similarity):
    sim = {}

    for item in topMatches(prefs,person,similarity):
        sim[item[0]] = item[1]
    weight = {}

    print('sim',sim)

    for person in sim:
        if sim[person] >= 0:
            for item in prefs[person]:
                weight[item] = {}

    #1
    for person in sim:
        #2
        if sim[person] >= 0:
            for item in prefs[person]:
                weight[item][person] = sim[person] * prefs[person][item]

    #3
    for name in prefs[person]:
        if prefs[person][name] != 0:
            #4
            weight.pop(name)
    sums = {}
    for item in weight:
        sums[item] = sum(weight[item].iteritems())

    #5
    kSum = {}
    for item in weight:
        kSum[item] = 0
    for item in weight:
        for person in sim:
            if sim[person] >= 0:
                if person in prefs.keys():
                    kSum[item] = kSum[item] + sim[person]

    recommendation = {}
    for item in sums:
        recommendation[item] = sums[item]/kSum[item]
    result = []
    #6
    for key, value in sorted(recommendation.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        result.append([key,value])

    return result

def run_ucf():

    print('-'*50,'\n', 'User based collaborative filtering \n', '-'*50)

    testbro = 'Toby'

    reco = getRecommendations(critics,testbro,sim_pearson)

    for i in reco:
        print (i,)

    print('-'*50)


run_ucf()