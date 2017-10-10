import glob
import os
import json

with open('UserFilmList.json', 'r') as fp:
    UserFilmList = json.load(fp)
max = -1
i = 0
j = 0
user_ = -1
UserList = []
for user in UserFilmList:
        i = i+1
#        print("films that user ", user," rated:")
#        for film in UserFilmList[user]:
        tmp = len(UserFilmList[user])
        if tmp > 1600 and tmp < 5000:
            UserList.append(user)

print("there are: ", len(UserList), "users")
print(UserList)

text_file = open("users.txt", "w")
for user in UserList:
    text_file.write(user+"\n")

text_file.close()