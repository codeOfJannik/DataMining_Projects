from sklearn.preprocessing import OneHotEncoder
from CSVtoSQLite import disk_engine
import pandas as pd


allLabels = pd.read_sql_query("SELECT label_id as lab FROM label_categories GROUP BY lab ORDER BY lab", disk_engine)

# binar encode
onehot_encoder = OneHotEncoder()
onehot_encoded = onehot_encoder.fit_transform(allLabels)
print(onehot_encoded)

