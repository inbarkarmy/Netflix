import json
import numpy as numpy
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

create1000usersvectors()
