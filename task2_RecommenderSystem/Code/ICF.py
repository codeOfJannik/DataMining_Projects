import numpy as np
from math import sqrt
from SimilarityOfCritics import critics, topMatches, sim_euclid, sim_pearson, sim_RusselRao


'''
NR.1
#1 details is a dic with movie titles as keys and the critics ratings as values
#2 check is dic for the movie exists
#3 Using .iteritems to iterate over key, value in dic
   .iteritems not work --> change to .items
'''
def transCritics(critics):
    movies = {}

    #1 #3
    for critics, details in critics.items():
        for title, rating in details.items():
            #2
            if title not in movies:
                movies[title] = {}
            movies[title][critics] = rating

    return movies

'''
NR.2
add transCritics to Dic
'''
def  calculateSimilarItems(prefs, similarity):
    simItems = {}

    for title in prefs:
        simItems[title] = topMatches(prefs,title,similarity)

    return simItems

'''
NR.3
calculation product recommendation
#1 item --> array about title and similarity of not bought Movies
#2 pearson distance    --> similarities < 0 should ignored
                       --> sumSimilarities might equal 0
#3 insert weighted recommendation into sorted result array
'''
def getRecommendedItems(prefs,person,similarity):
    simItem = calculateSimilarItems(prefs,similarity)
    result = []

    notboughtMovies = []
    for movie in simItem:
        if movie not in critics[person]:
            notboughtMovies.append(movie)

    for notboughtMovie in notboughtMovies:
        sumRecommendation = 0
        sumSimilarities = 0

        for purchasedMovie, rating in critics[person].iteritems():
            #1
            for item in simItem[notboughtMovie]:
                #2
                if item[0] == purchasedMovie:
                    if item[1] > 0:
                        sumRecommendation += rating * item[1]
                        sumSimilarities += item[1]
    #2
    recommandation = sumRecommendation / sumSimilarities if sumSimilarities != 0 else 0

    #3
    if len(result) == 0:
        result.append([notboughtMovie,recommandation])
    else:
        index = 0
        for i, value in enumerate(result):
            if value[1] > recommandation:
                index = i+1
            else:
                break
        result.insert(index, [notboughtMovie,recommandation])

    return result

transcitics = transCritics(critics)

'''
NR.4
Recommendation for Toby
'''

def run_icf():
    print('-'*50, '\n', 'Item based collaborative filtering \n', '-'*50)
    tc = transCritics(critics)
    person = 'Toby'


    print('Recommendations for %s ( Euclidean Distance): \n' % (person),
          getRecommendedItems(tc, person, sim_euclid))

    print('Recommendations for %s ( Pearson Distance): \n' % (person),
          getRecommendedItems(tc, person, sim_pearson))

    print('-'*50)

run_icf()


