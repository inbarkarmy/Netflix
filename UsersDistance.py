import json
import numpy as numpy
from sklearn.metrics import mean_squared_error
import math
NUMOFMODLES = 1000

def create1000usersvectors():
    with open('UserFilmList.json', 'r') as fp:
        userDict = json.load(fp)
    genreMat = numpy.load("myMat.dat")
    Genres = ['Comedy', 'Action', 'Adventure', 'Animation', 'Biography', 'Crime',
              'Documentary','Drama', 'Family', 'Fantasy', 'Film-Noir', 'History',
              'Horror', 'Music', 'Musical', 'Mystery', 'Romance',
              'Science Fiction', 'Sport', 'Thriller', 'War', 'Western',
              'Fitness']
    uservectors = numpy.zeros((NUMOFMODLES, len(Genres)))
    i=0
    for userID in open('users.txt'):
        sum_rates = numpy.zeros(len(Genres))
        num_movies = numpy.zeros(len(Genres))
        ID = userID.rstrip()
        for movie in userDict[ID]:
            movie_id, rate = movie.split(',', 1)
            rate = int(rate)
            print(rate)
            #print("movie_id: ", movie_id, "rate: ", rate)
            movie_id = int(movie_id) - 1
            j=0
            for genre in genreMat[movie_id]:
                #print(int(genre))
                if int(genre) == 1:
                    sum_rates[j] = sum_rates[j] + rate
                    num_movies[j] = num_movies[j] + 1
                    #print(Genres[j], ": ", sum_rates[j],", ", num_movies[j])
                j = j + 1
        j =0
        for genre in genreMat[0]:
            #print(sum_rates[j], num_movies[j])
            uservectors[i][j]= sum_rates[j]/float(num_movies[j])
            j= j + 1
        i = i + 1
    print(uservectors)
    uservectors.dump("usersvectors.dat")


def UserDistanceDict():
    with open('UserFilmList.json', 'r') as fp:
        userDict = json.load(fp)
    genreMat = numpy.load("myMat.dat")
    modelsvectors = numpy.load("usersvectors.dat")
    Genres = ['Comedy', 'Action', 'Adventure', 'Animation', 'Biography', 'Crime',
              'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History',
              'Horror', 'Music', 'Musical', 'Mystery', 'Romance',
              'Science Fiction', 'Sport', 'Thriller', 'War', 'Western',
              'Fitness']
    userdistancedict = dict()
    i =0
    for userID in userDict:
        print(userID, i)
        sum_rates = numpy.zeros(len(Genres))
        num_movies = numpy.zeros(len(Genres))
        uservector = numpy.zeros(len(Genres))
        for movie in userDict[userID]:
            movie_id, rate = movie.split(',', 1)
            rate = int(rate)
            print(rate)
            movie_id = int(movie_id) - 1
            j = 0
            for genre in genreMat[movie_id]:
                # print(int(genre))
                if int(genre) == 1:
                    sum_rates[j] = sum_rates[j] + rate
                    num_movies[j] = num_movies[j] + 1
                    # print(Genres[j], ": ", sum_rates[j],", ", num_movies[j])
                j = j + 1
        j = 0
        for genre in genreMat[0]:
            if num_movies[j] > 0:
                uservector[j] = sum_rates[j]/float(num_movies[j])
            else:
                uservector[j] = 0
            j = j + 1
        min = -1
        for x in range(0,1000):
            #print(uservector)
            #print(modelsvectors[x])
            mse = mean_squared_error(uservector, modelsvectors[x])
            rmse = math.sqrt(mse)
            if (min > rmse) or (min == -1):
                min = rmse
                closestuser = x+1
        userdistancedict[str(userID)] = closestuser
        i = i + 1
    with open('UsersDistance2.json', 'w') as fp:
        json.dump(UserDistanceDict, fp)

#create1000usersvectors()
UserDistanceDict()