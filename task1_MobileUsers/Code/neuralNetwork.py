import pandas as pd
from CSVtoSQLite import disk_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score

data = pd.read_sql_query('SELECT app_id as app, label_id as lab FROM app_labels ORDER BY app ', disk_engine)

data.head()

X = data.drop('app', axis=1)
Y = data['lab']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)


scaler = StandardScaler()
# Fit only to the training data
scaler.fit(x_train)

# Now apply the transformations to the data:
X_train = scaler.transform(x_train)
X_test = scaler.transform(x_test)

mlp = MLPClassifier(hidden_layer_sizes=(15, 15), max_iter=500)

mlp.fit(x_train, y_train)

predictions = mlp.predict(x_test)

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
print(accuracy_score(y_test, predictions))

