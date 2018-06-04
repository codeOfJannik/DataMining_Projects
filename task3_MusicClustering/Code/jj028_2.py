import pandas as pd
import numpy as np
import scipy
from sklearn.preprocessing import scale


# load csv data to pandas dataframe
trainData = pd.read_csv('FeatureFileTrainingAllList1a.csv', index_col='Unnamed: 0', sep=',', encoding='utf-8')
testData = pd.read_csv('FeatureFileTestAllList2a.csv', index_col='Unnamed: 0', sep=',', encoding='utf-8')


# scale standard deviation to 1
scale(trainData, axis=1, with_mean=False, with_std=True, copy=False)
scale(testData, axis=1, with_mean=False, with_std=True, copy=False)

print("")
print("*" * 20)
print("trainData")
print("")
print(trainData)
#print(trainData.iloc[-1])
print("")
print("*" * 20)
print("testData")
print("")
print(testData)
#print(testData.iloc[-1])


# calculate euclid disctance and/or correlation and write them into ordered list
def calc_distances(vec1, vec2, alg):
    distances = {}
    for vec1key, vec1value in vec1.iterrows():
        a = np.array(vec1value)
        list = []
        for vec2key, vec2value in vec2.iterrows():
            b = np.array(vec2value)
            if alg == "euclid":
                dist = np.linalg.norm(a - b)
            if alg == "correl":
                dist = np.correlate(a, b)
            list.append((dist, vec2key))

        orderedList = sorted(list, key=lambda x: x[0], reverse=False)
        distances[vec1key] = orderedList
    return distances

euclid_distance = calc_distances(trainData, testData, "euclid")
correlation = calc_distances(trainData, testData, "correl")

print("")
print("*" * 20)
print("euclid_distance")
print("")
print(euclid_distance)
print("")
print("*" * 20)
print("correlation")
print("")
print(correlation)


# calculate mean rank
def mean_rank(distances):
    meanSum = 0.0
    for key in distances:
        for index, pair in enumerate(distances[key]):
            if (pair[1] == key):
                meanSum += index + 1
                break;
    return (meanSum / len(distances))

print("")
print("*" * 20)
print("Mean rank (euclid):")
print("")
print (mean_rank(euclid_distance))
print("")
print("*" * 20)
print("Mean rank (correlation):")
print("")
print (mean_rank(correlation))