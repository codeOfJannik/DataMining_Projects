#from sklearn.preprocessing import OneHotEncoder, LabelEncoder
#from BuildFeatureVector import featureVector
#from BuildFeatureVector import getInstalledApps
from CSVtoSQLite import disk_engine
import pandas as pd
import numpy as np



# binar encode
featureVectorPhoneBrand_Int = LabelEncoder().fit(featureVector['installedApps'])
#print(list(featureVectorPhoneBrand_Int.classes_))
#onehot_encoder = OneHotEncoder(categorical_features=[2, 4])
#featureVector_Int = featureVector_Int.reshape(len(featureVector_Int), 1)
#onehot_encoded = onehot_encoder.fit_transform(featureVector_Int)
#print(onehot_encoded)
dummies= pd.get_dummies(allAppsLabeled)
print()

