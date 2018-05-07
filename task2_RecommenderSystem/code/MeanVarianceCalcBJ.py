import numpy as np
# Mittelwert:
# (1 + 2 + 3 + 4 + 5 + 6) / 6
# = 21 / 6
# = 3.5
# Varianz:
# ( (1-3.5)²+(2-3.5)²+(3-3.5)²+(4-3.5)²+(5-3.5)²+(6-3.5)² ) / 6
# = 17.5 / 6
# = 2.92

bVarcal = ((3 - 5.3) ** 2 + (3 - 5.3) ** 2 + (5 - 5.3) ** 2 + (6 - 5.3) ** 2 + (7 - 5.3) ** 2 + (8 - 5.3) ** 2) / 6
print('Varianz b:', bVarcal)

# Mittelwert:
# in python mit numpy:

a = np.array([1, 2, 3, 4, 5, 6])
b = np.array([3, 3, 5, 6, 7, 8])
aMean = np.mean(a)
print('Mittelwert a:', aMean)
# 3,5
bMean = np.mean(b)
print('Mittelwert b', bMean)
# 5,3333
# Varianz:
# in python mit numpy:
aVar = np.var(a)
print('Varianz a', aVar)
# 2,92
bVar = np.var(b)
print('Varianz b', bVar)
# 3,5
