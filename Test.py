from sklearn.preprocessing import OneHotEncoder
import numpy as numpy
import pandas as pd
import json
movieID = 0
genreMat = numpy.load("myMat.dat")
colNum = 26
moviesDatabase = pd.read_csv('database_new2.csv', encoding='latin1')
with open('UserFilmList.json', 'r') as fp:
    userDict = json.load(fp)
for line in open('probe.txt'):
    if line.strip()[-1]==':':
        movieID = line[:line.find(':')]
        print(movieID)
    else:
        usrID = line
        print("usrID:")
        print(usrID)
        usrInf= userDict[str(userID.rstrip())]
        #usrNearestModel = dict.get(usr)
        #todo: inbar change usrNearestModel after we have a dictionary
        usrNearestModel = 1333
        fileName = 'Test/usr' + str(usrNearestModel) + '.csv'
        vec = numpy.zeros((1, colNum))
        movieIdAndRate = usrInf[movieCount]
        usrRate = int(movieIdAndRate[movieIdAndRate.find(',') + 1:])
        vec[1][0:23] = genreMat[movieID]
        ImdbRate = moviesDatabase['rate'][movieID]
        if type(ImdbRate) == float:
            vec[1][23] = ImdbRate
        else:
            print(ImdbRate)
            rateImdb, ten = str(ImdbRate).split('/', 1)
            print(rateImdb, ten)
            vec[1][23] = Decimal(rateImdb)
        vec[1][24] = moviesDatabase['year'][movieID]
        vec[1][25] = usrRate
        for key in vec:
            csvlLine1[titlesDict[key]] = vec[key]
        print("csv line: ",csvlLine1)
        csvlLine1 = [str(x) for x in csvlLine1]
        with open(fileName, 'a') as fh:
            fh.write(",".join(csvlLine1) + '\n')
