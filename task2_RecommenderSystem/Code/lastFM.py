import pylast as pl
import SimilarityOfCritics as sc
from UserBasedCollaborativeFiltering import getRecommendations

network = pl.get_lastfm_network()

artist = network.get_artist('Drake')

# topfans = artist.get_top_fans(10)

usernames = ['BrunoJoS', 'DPREBOYE', 'MPistol40', 'NemoNightfall', 'SkyRif', 'Wags1382', 'Znapsen', 'cortapsyco',
             'emill_67', 'sattuviitana']
group = []
for u in usernames:
    u1 = network.get_user(u)
    group.append(u1)


def createLastfmUserDict(group):
    allBands = set()
    topUserBands = {}
    userDict = {}

    for user in group:
        topartist = user.get_top_artists()[0:20]
        topBandList = []
        for i in range(0, 20):
            try:
                allBands.add(str(topartist[i].item.name))
                topBandList.append(str(topartist[i].item.name))
            except:
                print "not able to write", topartist[i].item.name, "band into set"
        topUserBands[user] = topBandList

    for user in group:
        bandDict = {}
        for band in allBands:
            if band in topUserBands[user]:
                bandDict[band] = 1
            else:
                bandDict[band] = 0
        userString = str(user)
        userDict[userString] = bandDict

    return userDict


userDict = createLastfmUserDict(group)

user = 'SkyRif'


print sc.topMatches(userDict, user,'_simeuclid')
print getRecommendations(userDict, user, '_simeuclid')

print '\n'
print '-'*35,'top Matches for ',user,' (Euclidean Distance)','-'*35,'\n', sc.topMatches(userDict, user,'_simeuclid'), '\n'
print '-'*33,'Recommendations for ',user,' (Euclidean Distance)','-'*33,'\n', getRecommendations(userDict, user, '_simeuclid'), '\n'
print '-'*33,'Recommendations for ',user,' (Russel_Rao Distance)','-'*33,'\n', getRecommendations(userDict, user, '_simrussel')
print '-'*117

