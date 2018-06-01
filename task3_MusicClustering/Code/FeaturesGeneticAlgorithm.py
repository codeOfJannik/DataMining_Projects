from Matching import trainDF, testDF, meanRank, distance
import numpy as np
import pandas as pd
import random

FeatNames = ["amp1mean", "amp1std", "amp1skew", "amp1kurt", "amp1dmean", "amp1dstd", "amp1dskew", "amp1dkurt",
             "amp10mean", "amp10std",
             "amp10skew", "amp10kurt", "amp10dmean", "amp10dstd", "amp10dskew", "amp10dkurt", "amp100mean", "amp100std",
             "amp100skew",
             "amp100kurt", "amp100dmean", "amp100dstd", "amp100dskew", "amp100dkurt", "amp1000mean", "amp1000std",
             "amp1000skew",
             "amp1000kurt", "amp1000dmean", "amp1000dstd", "amp1000dskew", "amp1000dkurt", "power1", "power2", "power3",
             "power4",
             "power5", "power6", "power7", "power8", "power9", "power10"]

populationSize = 20
featureCount = 20
iterations = 100
mutationProbability = 5  # in %


def initPopulation(popsize, featurecount):
    population = np.zeros((popsize, featurecount))
    for i in range(populationSize):
        population[i, 0:featureCount] = np.random.permutation(random.sample(range(len(FeatNames)), featurecount))
    return population


def startGeneticAlgorithm(initialPopulation, featurecount, iterations, mutationProbability):
    population = initialPopulation
    i = 0
    while i < iterations:
        populationFitnessDict = calculateFitness(population)
        childList = crossing(populationFitnessDict, mutationProbability, featurecount)
        j = 0
        while j < len(childList):
            worstChromosome = populationFitnessDict[sorted(populationFitnessDict.keys())[-1]]
            del populationFitnessDict[sorted(populationFitnessDict.keys())[-1]]
            worstIndex = np.where(np.all(population == worstChromosome, axis=1))
            population = np.delete(population, worstIndex[0][0], axis=0)
            population = np.vstack([population, childList[j]])
            j += 1
        i += 1



def calculateFitness(population):
    fitnessDict = {}
    for chromosome in population:
        featureList = []
        for featureIndex in chromosome:
            featureList.append(FeatNames[int(featureIndex)])
        subTrainDataFrame = pd.DataFrame(index=trainDF.index, columns=featureList, data=trainDF[featureList])
        subTestDataFrame = pd.DataFrame(index=testDF.index, columns=featureList, data=testDF[featureList])

        distances = distance('dist_euclid', subTrainDataFrame, subTestDataFrame)
        fitnessValue = meanRank(distances)
        fitnessDict[fitnessValue] = chromosome
    return fitnessDict


def selection(populationFitnessDict):
    allfitnessValues = populationFitnessDict.keys()
    allfitnessValues = np.array(sorted(allfitnessValues))

    allfitnessValuesSum = np.array(allfitnessValues).sum()
    rn1 = allfitnessValuesSum * np.random.rand()
    found1 = False
    found2 = False
    index = 1
    while not found1:
        if rn1 < allfitnessValues[:index].sum(axis=0):
            found1 = index
        else:
            index += 1
    found1 = found1 - 1
    equal = True
    while equal:
        rn2 = allfitnessValuesSum * np.random.rand()
        found2 = False
        index = 1
        while not found2:
            if rn2 < allfitnessValues[:index].sum(axis=0):
                found2 = index
            else:
                index += 1
        found2 = found2 - 1
        if found2 != found1:
            equal = False
    parent1 = populationFitnessDict[allfitnessValues[found1]]
    parent2 = populationFitnessDict[allfitnessValues[found2]]
    return parent1, parent2


def crossing(populationFitnessDict, mutationProbability, featurecount):
    while True:
        parents = selection(populationFitnessDict)
        parent1 = sorted(parents[0])
        parent2 = sorted(parents[1])
        crossBoarder = random.randint(5, 15)
        parent1A = parent1[:crossBoarder]
        parent1B = parent1[crossBoarder:]
        parent2B = parent2[:crossBoarder]
        parent2A = parent2[crossBoarder:]
        child1 = np.append(parent1A, parent2A)
        child2 = np.append(parent1B, parent2B)
        if len(set(child1)) == featurecount and len(set(child2)) == featurecount:
            childList = mutation(mutationProbability, child1, child2)
            for index, child in enumerate(childList):
                featureList = []
                for featureIndex in child:
                    featureList.append(FeatNames[int(featureIndex)])
                subTrainDataFrame = pd.DataFrame(index=trainDF.index, columns=featureList, data=trainDF[featureList])
                subTestDataFrame = pd.DataFrame(index=testDF.index, columns=featureList, data=testDF[featureList])

                distances = distance('dist_euclid', subTrainDataFrame, subTestDataFrame)
                fitnessValue = meanRank(distances)
                if fitnessValue > sorted(populationFitnessDict.keys())[-1]:
                    childList.pop(index)
            return childList


# TODO: funktioniert noch nicht
def mutation(mutationProbability, child1, child2):
    childList = [child1, child2]
    for index in range(len(childList)):
        indx = index
        mutrn = random.randint(0, 100)
        if mutrn < 101:
            childList.pop(indx)
            reducedFeatNames = []
            for idx, element in enumerate(FeatNames):
                if idx not in childList[indx]:
                    reducedFeatNames.append(element)
            reducedFeatNames = np.array(reducedFeatNames)
            randomReplaceIndex = random.randint(0, len(childList[indx])-1)
            randomFeatNameIndex = random.randint(0, len(reducedFeatNames)-1)
            childList[indx][randomReplaceIndex] = FeatNames.index(reducedFeatNames[randomFeatNameIndex])
            childList.append(childList[indx])
    return childList



population = initPopulation(populationSize, featureCount)
startGeneticAlgorithm(population, featureCount, iterations, mutationProbability)
