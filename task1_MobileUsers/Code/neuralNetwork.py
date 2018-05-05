from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from BuildFeatureVector import featureVector

data = featureVector

data.head()

X = data.drop(['agegroup', 'device'], axis=1)
Y = data['agegroup']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)


scaler = StandardScaler()
# Fit only to the training data
scaler.fit(x_train)

# Now apply the transformations to the data:
X_train = scaler.transform(x_train)
X_test = scaler.transform(x_test)

mlp = MLPClassifier(hidden_layer_sizes=(15, 15), max_iter=100)

mlp.fit(x_train, y_train)

predictions = mlp.predict(x_test)

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
print(accuracy_score(y_test, predictions))
