def calculateMean(vector):
    summe = 0
    for element in vector:
        summe += element
    result = float(summe) / float(len(vector))
    return result


def variance(vector):
    mean = calculateMean(vector)
    summe = 0
    for element in vector:
        summe += (element - mean) ** 2
    result = float(summe) / float(len(vector))
    return result


a = [1, 2, 3, 4, 5, 6]
b = [3, 3, 5, 6, 7, 8]


print "Mean a:", calculateMean(a)
print "Mean b:", calculateMean(b)
print "Variance a:", variance(a)
print "Variance b:", variance(b)




