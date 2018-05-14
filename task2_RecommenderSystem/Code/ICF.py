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

    for title in prefs.keys():
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
    for movie in simItem.keys():
        if movie not in critics[person]:
            notboughtMovies.append(movie)

    recommandations = {}
    for notboughtMovie in notboughtMovies:
        sumRecommendation = 0
        sumSimilarities = 0
        for purchasedMovie, rating in critics[person].items():
            if similarity == '_simeuclid':
                simi = sim_euclid(prefs, purchasedMovie, notboughtMovie)
                sumRecommendation += simi * rating
                sumSimilarities += simi
            elif similarity == '_simpearson':
                simi = sim_pearson(prefs, purchasedMovie, notboughtMovie)
                sumRecommendation += simi * rating
                sumSimilarities += simi
        #3
        recommandations[notboughtMovie] = sumRecommendation / sumSimilarities if sumSimilarities != 0 else 0

    return recommandations

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
          getRecommendedItems(tc, person, '_simeuclid'))

    print('Recommendations for %s ( Pearson Distance): \n' % (person),
          getRecommendedItems(tc, person, '_simpearson'))

    print('-'*50)

run_icf()


