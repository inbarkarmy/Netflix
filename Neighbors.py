from sklearn.preprocessing import OneHotEncoder
import numpy as numpy
import pandas as pd
import json
import math
from decimal import Decimal

#max distance between movies - define as needed
maxDist = 4

def caculateVecDistance(binaryVec1, binaryVec2 ):
    dist=maxDist
    if len(binaryVec1)==len(binaryVec2):
        for i in range(len(binaryVec1)):
            if binaryVec1[i]==binaryVec2[i]:
                if binaryVec2[i]==1:
                    dist=dist-1
    return dist

def TwoMoviesDist(genreVec1, genreVec2):

    genreDist = caculateVecDistance(genreVec1,genreVec2)
    #if rate1>rate2:
    #    rateDist = rate1-rate2
    #else:
    #    rateDist = rate2-rate1
    #if year1 > year2:
    #    yearDist = year1 - year2
    #else:
    #    yearDist = year2 - year1
    #totalDist = (genreWeghit*genreDist)+(rateWeight*rateDist)+(yearWeight*yearDist)
    #return totalDist
    return genreDist


def createMovieDistancesMatrix():
    data = pd.read_csv('Movies_info.csv', encoding='latin1')
    moviesNum =len(data["title"])
    genreMatrix = createGenreMatrix()
    res = numpy.zeros((moviesNum, moviesNum))
    i=0
    for movie1 in data["title"]:
        j=0
        for movie2 in data["title"]:
            if i==j:
                curDist=0
            else:
                curDist = TwoMoviesDist(genreMatrix[i],genreMatrix[j])
            res[i][j] = curDist
            j=j+1
        i=i+1
    return res

def createGenreMatrix():
    data = pd.read_csv('database_new2.csv',encoding='latin1')
    totalGenres = 23
    moviesNum= len(data["title"])
    print(moviesNum)
    genreMatrix = numpy.zeros((moviesNum,totalGenres))
    movieCount =0
    dictGenre = {0: 'Comedy', 1: 'Action', 2: 'Adventure', 3: {'Animated', 'Animation'}, 4: 'Biography', 5: 'Crime',
                 6: 'Documentary', 7: 'Drama', 8: 'Family', 9: 'Fantasy', 10: 'Film-Noir', 11: 'History',
                 12: 'Horror', 13: 'Music', 14: 'Musical', 15: 'Mystery', 16: 'Romance',
                 17: {'Science Fiction', 'Sci-Fi'}, 18: {'Sports', 'Sport'}, 19: 'Thriller', 20: 'War', 21: 'Western',
                 22: 'Fitness'}

    for row in data["title"]:
        for i in range(3):
            curGenre = "genre"+str(i)
            genreA = data[curGenre][movieCount]
            genre = str(genreA).rstrip()
            for key in range(totalGenres):
                if len(dictGenre.get(key))==2:
                    for val in dictGenre.get(key):
                        if genre==val:
                            genreMatrix[movieCount][key]=1
                            break
                else:
                    if genre == dictGenre.get(key):
                        genreMatrix[movieCount][key] = 1
                        break
        movieCount = movieCount + 1
    return genreMatrix

def createUserTrainingSet():
    with open('UserFilmList.json', 'r') as fp:
        userDict = json.load(fp)
    genreMat = numpy.load("myMat.dat")
    moviesDatabase = pd.read_csv('database_new2.csv', encoding='latin1')
    colNum = 26
    for userID in open('users.txt'):
        usr = userDict[str(userID.rstrip())]
        moviesNum = len(usr)
        userMatrix =  numpy.zeros((moviesNum, colNum))
        movieCount=0
        for movie in usr:
            movieIdAndRate = usr[movieCount]
            movieID = int(movieIdAndRate[:movieIdAndRate.find(',')])
            movieID = movieID-1
            usrRate = int(movieIdAndRate[movieIdAndRate.find(',')+1:])
            #todo: check the titles didn;t mess up the movies indexes-
            #make surethe movie ID matches the genres we were expecting
            #   add to each row: the user's rate
            userMatrix[movieCount][0:23] = genreMat[movieID]
            ImdbRate = moviesDatabase['rate'][movieID]
            #Rating = float(ImdbRate)
            if type(ImdbRate) == float:
                userMatrix[movieCount][23] = ImdbRate
            else:
                print(ImdbRate)
                rateImdb, ten = str(ImdbRate).split('/', 1)
                print(rateImdb, ten)
                userMatrix[movieCount][23] = Decimal(rateImdb)
                if type(moviesDatabase['year'][movieID]) is str:
                    userMatrix[movieCount][24] = 0
                else:
                    userMatrix[movieCount][24] = moviesDatabase['year'][movieID]
            userMatrix[movieCount][25] = usrRate
            movieCount = movieCount+1
        fileName = 'usr'+str(userID.rstrip())+'.csv'
        numpy.savetxt(fileName, userMatrix, delimiter=",")
        #todo : remove break
        break

movieDistancesMatrix = createGenreMatrix()
print("finished genre matrix")
movieDistancesMatrix.dump("myMat.dat")
createUserTrainingSet()



def FindKNearestNeighbors(movieNum,userID):
    print("started")
    with open('UserFilmList.json', 'r') as fp:
        userDict = json.load(fp)
    print("finished opening")
    usr = userDict.get(userID)
    print("usr")
    print(usr)
    #todo - change k
    K = math.sqrt((len(usr)))
    kDistArr = numpy.zeros(K)
    movieArr = numpy.zeros(K)
    rateArr = numpy.zeros(K)
    print(K)
    for i in range(K):
        kDistArr[i] = maxDist+1
    for val in usr:
        curDist = TwoMoviesDist(movieNum,val)
        for j in range(K):
            if curDist< kDistArr:
                kDistArr[j] = curDist
                movieArr[j] = val
                break
    j=0
    for movieID in movieArr:
        fileName = "mv_"
        maxID=1000000
        for i in range(7):
            if movieID < maxID:
                fileName = fileName + str(0)
                maxID = maxID/10
            else:
                break
        fileName = fileName + str(movieID)
        fileName = "\training_set\training_set" + fileName
        print(fileName)
        #skipping the first row
        iterLine = open(fileName)
        next(iterLine)
        for line in iterLine:
            ratetmp = line[line.find(',') + 1:]
            rate = ratetmp[:ratetmp.find(',')]
            curID = line[ :line.find(',')]
            print("curID:")
            print(curID)
            print("rate:")
            print(rate)
            if curID == userID:
                rateArr[j] = rate
                break
        j=j+1
    sum =0
    for p in range(K):
        sum = sum + rateArr[p]
    avg = sum/K
    print(avg)
    return avg