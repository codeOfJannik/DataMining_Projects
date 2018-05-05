from CSVtoSQLite import disk_engine, resources_path
from AccessDevices import genderAgeTrain_df
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Read data of phone_device_brand_model
phoneBrandDevices = pd.read_sql("SELECT device_id, phone_brand FROM phone_brand_device_model", disk_engine)


# Read brandMap.txt and create dictionary to replace chinese brand names
def replaceChineseBrandNames(dataframe):
    brandDict = {}
    with open(os.path.join(resources_path, "brandMap.txt")) as f:
        for line in f:
            if line == "\n":
                continue
            (key, val) = line.split()
            brandDict[key] = val
    for key in brandDict.keys():
        dataframe.replace(to_replace=key, value=brandDict[key], inplace=True)
    return dataframe


phoneBrandDevices = replaceChineseBrandNames(phoneBrandDevices)
print("Number of different devices in phone_brand_device_model:", len(set(phoneBrandDevices['device_id'])))
print("Number of different brands in phone_brand_device_model:", len(set(phoneBrandDevices['phone_brand'])))

# Add column with brands to genderAgeDataFrame
deviceBrandDict = {}
index = 0
for device in phoneBrandDevices['device_id']:
    deviceBrandDict[device] = phoneBrandDevices['phone_brand'][index]
    index += 1

index = 0
brandList = []
for element in genderAgeTrain_df['device_id']:
    brandList.append(deviceBrandDict[genderAgeTrain_df['device_id'][index]])
    index += 1
genderAgeTrain_df['brand'] = brandList
genderAgeTrain_df.to_csv(os.path.join(resources_path, "gender_age_brand_train.csv"), sep=",", encoding="utf-8")

numberDevicesBrand = genderAgeTrain_df['brand'].value_counts()

x = np.array(numberDevicesBrand.index[0:20])
y = np.array(numberDevicesBrand.values[0:20])
ind = np.arange(len(x))
plt.bar(ind, y, 0.35)
plt.xticks(ind, x, rotation=90)
plt.yticks(np.arange(0, 19000, 1000))
plt.grid(True)

plt.show()
