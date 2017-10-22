from sklearn.preprocessing import OneHotEncoder
import numpy as numpy
import pandas as pd
import json
import csv
movieID = 0
genreMat = numpy.load("myMat.dat")
with open('DistanceUsers.json', 'r') as fp:
    UserDistance = json.load(fp)
colNum = 26
csvlLine1 = [0]*colNum
moviesDatabase = pd.read_csv('database_new2.csv', encoding='latin1')
with open('UserFilmList.json', 'r') as fp:
    userDict = json.load(fp)
for line in open('probe.txt'):
    if line.strip()[-1] == ':':
        movieID = line[:line.find(':')]
    else:
        usrID = line
        #print("usrID: ", usrID)
        usrID = usrID.rstrip()
        #print("UserID: ", str(usrID.rstrip()))
        usrInf= userDict[str(usrID.rstrip())]
        #usrNearestModel = dict.get(usr)
        #todo: inbar change usrNearestModel after we have a dictionary
        usrNearestModel = UserDistance[str(usrID)]
        fileName = 'Test/usr' + str(usrNearestModel) + '.csv'
        vec = [0]*colNum
        for movieIDandRate in userDict[str(usrID)]:
            movie, rate = movieIDandRate.split(',',1)
            if movie == movieID:
                usrRate = rate
                break
        vec[0:23] = genreMat[int(movieID)-1,:]
        ImdbRate = moviesDatabase['rate'][int(movieID)]
        if type(ImdbRate) == float:
            vec[23] = ImdbRate
        else:
            rateImdb, ten = str(ImdbRate).split('/', 1)
            vec[23] = float(rateImdb)
        vec[24] = moviesDatabase['year'][int(movieID)]
        vec[25] = usrRate
        for i in range(0,26):
            csvlLine1[i] = vec[i]
        #csvlLine1 = [float(x) for x in csvlLine1]
        #csvlLine1 = [x.rstrip('\n') for x in csvlLine1]
        print("csvline: ", csvlLine1, " End." )
        #f_handler = open(fileName,'a')
        #numpy.savetxt(f_handler, csvlLine1)
        #f_handler.close()
        with open(fileName, 'a') as fh:
            csvWriter = csv.writer(fh, delimiter=',')
            csvWriter.writerow(csvlLine1)
