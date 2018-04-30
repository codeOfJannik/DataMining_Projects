from AccessDevices import genderAgeTrain_df
import matplotlib.pyplot as plt
import numpy as np

# Read ageGroups of gender_age_train
genderAgeGroup = genderAgeTrain_df["agegroup"]
x = np.unique(genderAgeGroup)
l = list()
for e in x:
    count = 0
    for f in genderAgeGroup:
        if e == f:
            count = count + 1
    l.append(count)
y = np.array(l)
ind = np.arange(len(x))
plt.bar(ind, y, 0.35)
plt.xticks(ind, x, rotation=90)
plt.yticks(np.arange(0, 12000, 1000))
plt.grid(True)

plt.show()
