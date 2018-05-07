from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
import pandas as pd
from CSVtoSQLite import disk_engine


data = pd.read_sql_query("SELECT * FROM featureVector", disk_engine)
data = data.fillna(0)

data.head()

X = data.drop(['agegroup', 'device'], axis=1)
Y = data['agegroup']

X_scaled = preprocessing.scale(X)

x_train, x_test, y_train, y_test = train_test_split(X_scaled, Y, test_size=0.25)


mlp = MLPClassifier(hidden_layer_sizes=(20, 20), max_iter=200)

mlp.fit(x_train, y_train)

predictions = mlp.predict(x_test)

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
print(accuracy_score(y_test, predictions))

scores = cross_val_score(mlp, X_scaled, Y, cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))