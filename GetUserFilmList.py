import glob
import os
try:
    import simplejson as json
except ImportError:
    import json

def CreateUsersFilmsDictionary():

    # parameters:
    i =0
    j=0
    curr_path = os.path.dirname(os.path.abspath(__file__))
    path = curr_path + r'\training_set\training_set\*.txt'
    UserFilmDictionary = dict()
    UserFilmDictionary_tmp = dict
    #create a lint of all files
    files = glob.glob(path)
    # iterate over the list getting each file
    k = 0
    for fle in files:
        i = i+1
        #open the file and then call .read() to get the text
        tmp = open(fle)
        #skip first line of the file
        next(tmp)
        for line in tmp:
            user, rate, date = line.split(',', 2)
            value = str(i)+','+rate
            if user not in UserFilmD(k):
                UserFilmDictionary.setdefault(user, [])
            #print(value)
            UserFilmDictionary[user].append(value)
    #for user in UserFilmDictionary:
        #print ("films that user ", user," rated:")
        #for film in UserFilmDictionary[user]:
            #print(film)
    # save to jason file
    with open('UserFilmList.json', 'w') as fp:
        json.dump(UserFilmDictionary, fp)


CreateUsersFilmsDictionary()
