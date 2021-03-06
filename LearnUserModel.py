import math
from numpy import loadtxt
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy
import time
import csv

# load data
def LearnUserModel(keyUser):
    start_time = time.time()
        #modelUsr = userModelDict.get(keyUser)
    usrFileName = 'usersCSV/usr'+ str(keyUser) + '.csv'
    testFileName = 'Test/usr' + str(keyUser) + '.csv'
    #print(usrFileName)
    train_set = loadtxt(usrFileName, delimiter=",")
    test_set = loadtxt(testFileName, delimiter=",")
    col_labels = {'Comedy', 'Action', 'Adventure', 'Animated', 'Biography', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History',
                  'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Science Fiction', 'Sports', 'Thriller', 'War', 'Western', 'Fitness'}

    # split data into input and output
    #X = train_set[:, 0:25]
    #Y = train_set[:, 25]
    #print("type: ", type(test_set))
    #a = numpy.array(test_set)
    #print("size: ", len([test_set]))
    # split data into train and test sets
    #seed = 7
    #test_size = 0.2
    #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
    X_train = train_set[:, 0:25]
    X_test = train_set[:, 25]
    #print(test_set[0:25].shape)
    try:
        shape = (test_set.shape[0], test_set.shape[1])
    except IndexError:
        shape = (1, test_set.shape[0])
    #print(shape)
    if shape[0] is 1:
        #print("hello")
        y_train = [test_set[0:25]]
        y_test = [test_set[25]]
    else:
        #print("HIIII")
        y_train = test_set[:, 0:25]
        y_test = test_set[:, 25]

    #print(X_train)
    #print(y_train, len(y_train))

    # fit model no training data
    model = XGBClassifier()
    model.fit(X_train, X_test)
    #print(model)

    # make predictions for test data
    y_pred = model.predict(y_train)
    predictions = [round(value) for value in y_pred]
    #print(y_pred)
    # evaluate predictions
    mse = mean_squared_error(y_test, predictions)
    rmse = math.sqrt(mse)
    #print("%s seconds to learn 1 usr model" %(time.time() - start_time))
    #print("Accuracy: %.2f" % (rmse))
    return rmse

start_time_all=time.time()
rmse_all = 0
time_all=0
csvOut = [2]*1000
for i in range(0,1000):
    #print(i)
    start_time_i = time.time()
    if i == 122:
        continue
    if i == 198:
        continue
    rmse_i=LearnUserModel(i)
    rmse_all = rmse_all + rmse_i
    time_all = time_all + time.time() - start_time_i
    csvOut[i] = [(time.time() - start_time_i), rmse_i]
    with open("timeMeasuring.csv", 'a',newline='') as fh:
        csvWriter = csv.writer(fh, delimiter=',')
        csvWriter.writerow(csvOut[i])
print("%s seconds to learn all users" %(time.time()-start_time_all))
print("\n", "Average RMSE: ", rmse_all/998)
print("\n", "Average time per user : ", str(time_all/998))
