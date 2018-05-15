from math import sqrt
import numpy as np
import operator


critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
}


def sim_euclid(prefs, person1, person2, normed=True):
    ''' Returns a euclidean-distance-based similarity score for
    person1 and person2. In the distance calculation the sum is computed
    only over those items, which are nonzero for both instances, i.e. only
    films which are ranked by both persons are regarded.
    If the parameter normed is True, then the euclidean distance is divided by
    the number of non-zero elements integrated in the distance calculation. Thus
    the effect of larger distances in the case of an increasing number of commonly ranked
    items is avoided.
    '''
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1
    # len(si) counts the number of common ratings
    # if they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = np.sqrt(sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                                  for item in prefs[person1] if item in prefs[person2]]))
    if normed:
        sum_of_squares = 1.0 / len(si) * sum_of_squares
    return 1 / (1 + sum_of_squares)


def sim_pearson(prefs, p1, p2):
    '''
    Returns the Pearson correlation coefficient for p1 and p2
    '''

    # Get the list of commonly rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0: return 0

    # Sum calculations
    n = len(si)

    # Calculate means of person 1 and 2
    mp1 = np.mean([prefs[p1][it] for it in si])
    mp2 = np.mean([prefs[p2][it] for it in si])

    # Calculate standard deviation of person 1 and 2
    sp1 = np.std([prefs[p1][it] for it in si])
    sp2 = np.std([prefs[p2][it] for it in si])

    # If all elements in one sample are identical, the standard deviation is 0.
    # In this case there is no linear correlation between the samples
    if sp1 == 0 or sp2 == 0:
        return 0
    r = 1 / (n * sp1 * sp2) * sum([(prefs[p1][it] - mp1) * (prefs[p2][it] - mp2) for it in si])
    return r


print("euclidean similiarity Toby & Lisa Rose:", sim_euclid(critics, 'Toby', 'Lisa Rose'))
print("pearson similiarity Toby & Lisa Rose:", sim_pearson(critics, 'Toby', 'Lisa Rose'))
print("")


def sim_RusselRao(prefs, person1, person2, normed=True):
    ''' Returns RusselRao similaritiy between 2 users. The RusselRao similarity just counts the number
    of common non-zero components of the two vectors and divides this number by N, where N is the length
    of the vectors. If normed=False, the division by N is omitted.
    '''
    # Get the list of shared_items
    si = {}
    commons = 0
    for item in prefs[person1]:
        if prefs[person1][item] == 1 and prefs[person2][item] == 1:
            commons += 1
    # print commons
    if not normed:
        return commons
    else:
        return commons * 1.0 / len(prefs[person1])


def topMatches(prefs, person, similarity):
    prefsReduced = {key: value for key, value in prefs.items()
                    if key is not person}
    similarities = list()
    for key, value in prefsReduced.items():
        if similarity == '_simeuclid':
            similarities.append(sim_euclid(prefs, person, key))
        elif similarity == '_simpearson':
            similarities.append(sim_pearson(prefs, person, key))
        else:
            return list()

    return sorted(similarities)


for key in critics.keys():
    print("euclidean similarities of", key, ":", topMatches(critics, key, '_simeuclid'))
    print("pearson similarities of", key, ":", topMatches(critics, key, '_simpearson'))




# ab hier der code für die ucf aufgabe

'''
function takes the given critics dictionary, a given person and a given similarity algorithm and returns a 
recommendation as a sorted list in descending order for not yet seen movies for the given person. 
in this example there will be movie recommendations for the person toby.
'''

def getRecommendations(prefs, person, similarity):

    # compute correlations
    sim = {}
    for candidate in prefs:
        if candidate == person:
            continue
        sim[candidate] = similarity(prefs, person, candidate)

    kSums = {}
    unknownMedia = {}
    for candidate in prefs:
        # don't compare a person with itself
        if candidate == person:
            continue
        # if the correlation is negative, the persons are too different
        if sim[candidate] < 0:
            continue
        # for every media the candidate already knows
        for media in prefs[candidate]:
            # for every media the candidate did not know
            if media not in prefs[person] or prefs[person][media] == 0:
                # check if the not yet seen media is already in the unknownMedia list
                # if not, add it to unknownMedia and kSums with value 0
                if media not in unknownMedia:
                    unknownMedia[media] = 0
                    kSums[media] = 0
                # add the correlation of the candidate to the kSum of the current media
                kSums[media] += sim[candidate]
                # add the recommendation
                unknownMedia[media] += sim[candidate] * prefs[candidate][media]

    # divide the sum of the media by the kSum of the media
    for media in unknownMedia:
        unknownMedia[media] = unknownMedia[media]/kSums[media]


    # sort dictionary into list by descending keys (recommendation score)
    list = sorted(unknownMedia.items(), key=lambda t: t[1], reverse=True)

    return list


print("")
print("Recommended Movies for Toby: " + str(getRecommendations(critics, 'Toby', sim_pearson)))
