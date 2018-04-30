from CSVtoSQLite import resources_path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


genderAgeBrand_df = pd.read_csv(
    os.path.join(resources_path, "gender_age_brand_train.csv"), sep=",", encoding="utf-8", index_col=0
)
genderAgeGroups = set(genderAgeBrand_df['agegroup'])
mostFrequentBrands = (genderAgeBrand_df['brand'].value_counts()).index[0:20]
 # TODO: Hübscher machen
plt.xticks(np.arange(20), mostFrequentBrands, rotation=90)
plt.yticks(np.arange(0, 30, 5))
plt.ylabel("% of frequencies of brand")
plt.grid(True)

for group in genderAgeGroups:
    yList = []
    members = pd.DataFrame(genderAgeBrand_df.loc[genderAgeBrand_df['agegroup'] == group])
    count = len(members)
    for brand in mostFrequentBrands:
        brandCount = len(members.loc[members['brand'] == brand])
        brandPercent = brandCount / count * 100
        yList.append(brandPercent)
    yValues = np.array(yList)
    plt.plot(yValues)



plt.show()

