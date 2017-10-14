from numpy import loadtxt
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# load data
train_set = loadtxt('usr1227322.csv', delimiter=",")

col_labels = {'Comedy', 'Action', 'Adventure', 'Animated', 'Biography', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History',
              'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Science Fiction', 'Sports', 'Thriller', 'War', 'Western', 'Fitness'}

# split data into input and output
X = train_set[:, 0:25]
Y = train_set[:, 25]

# split data into train and test sets
seed = 7
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)


# fit model no training data
model = XGBClassifier()
model.fit(X_train, y_train)

print(model)

# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

print(y_pred)

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))