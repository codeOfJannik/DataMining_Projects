from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing

from BuildFeatureVector import featureVector

data = featureVector

data.head()

X = data.drop(['agegroup', 'device'], axis=1)
Y = data['agegroup']

X_scaled = preprocessing.scale(X)
print(X_scaled.mean(axis=0))
print(X_scaled.std(axis=0))
print(X_scaled.var())

x_train, x_test, y_train, y_test = train_test_split(X_scaled, Y, test_size=0.25)


mlp = MLPClassifier(hidden_layer_sizes=(15, 15), max_iter=100)

mlp.fit(x_train, y_train)

predictions = mlp.predict(x_test)

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
print(accuracy_score(y_test, predictions))

scores = cross_val_score()
