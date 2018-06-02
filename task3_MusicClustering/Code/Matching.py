import pandas as pd
from sklearn import preprocessing
from scipy import spatial

# Einlesen (Aufgabe 1)
trainDF = pd.read_csv("FeatureFileTrainingAllList1.csv", sep=',', index_col=0)
testDF = pd.read_csv("FeatureFileTestAllList2.csv", sep=',', index_col=0)

# Skalieren (Aufgabe 2)
scaledTrainDF = preprocessing.scale(trainDF)
scaledTestDF = preprocessing.scale(testDF)
# skalierte Werte wieder den Indices zuordnen
trainDF = pd.DataFrame(index=trainDF.index, columns=trainDF.columns, data=scaledTrainDF)
testDF = pd.DataFrame(index=testDF.index, columns=testDF.columns, data=scaledTestDF)


# Distanzen berechnen (Aufgabe 3)
def distance(similarity, trainDataframe, testDataframe):
    allDistDict = {}
    for index, row in trainDataframe.iterrows():
        distDict = {}
        for index2, row2 in testDataframe.iterrows():
            if similarity == 'dist_euclid':
                distDict[index2] = spatial.distance.euclidean(row, row2)
            if similarity == 'dist_correlation':
                distDict[index2] = spatial.distance.correlation(row, row2)

        distList = sorted(distDict.items(), key=lambda t: t[1], reverse=False)
        allDistDict[index] = distList
    return allDistDict


allDistancesDictEuclid = distance('dist_euclid', trainDF, testDF)
allDistancesDictCorrelation = distance('dist_correlation', trainDF, testDF)


def meanRank(allDistDict):
    rankSum = 0
    for key, value in allDistDict.items():
        rank = 1
        for element in value:
            if element[0] == key:
                rankSum += rank
            else:
                rank += 1

    meanRank = rankSum / len(allDistDict)
    return meanRank


euclidMeanRank = meanRank(allDistancesDictEuclid)
correlationMeanRank = meanRank(allDistancesDictCorrelation)

print(euclidMeanRank)
print(correlationMeanRank)
