import csv

FILE_NAME = "database_new2.csv"

TITLES_LIST = 'title,year,Time,country,director,lang,rate,genre0,genre1,genre2,actor0,actor1,actor2'
with open(FILE_NAME, 'a') as fh:
    fh.write(TITLES_LIST+ '\n')
i = 0
write_line = 0
for line in open('movie_titles2.txt'):
    i = i+1
    no_id = line[line.find(',') + 1:]
    year = no_id[:no_id.find(',')]
    name = no_id[no_id.find(',') + 1:]
    name = name[:-1]
    #print("year ", year, "name: ", name)
    movies_data = open('database_new.csv')
    next(movies_data)
    for row in movies_data:
        MovieName, MovieYear, data = row.split(',', 2)
        if MovieName == name and MovieYear == year:
            with open(FILE_NAME, 'a') as fh:
                fh.write(row)
                write_line = 1
                print(i)
            break
    if write_line == 0:
        with open(FILE_NAME, 'a') as fh:
            fh.write(name+','+year+'\n')
    write_line = 0