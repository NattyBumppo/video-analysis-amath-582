# -*- coding: utf-8 -*-
"""

John Fuini, Grade 4, Mrs. Cotton, Orange Iguanas

"""

import csv
import re

csv_filename = "trailer_data.csv"

no_genre_movie_list = []
genre_list = []

#findin the genres and the movies without genres
with open(csv_filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for i, row in enumerate(reader):
        if row["genre"]:
            # build genre list being all regexy like Nat
            genres = re.findall('(\w+)', row["genre"])
            for genre in genres:
                if genre in genre_list:
                    pass
                else:
                    genre_list.append(genre)
            # holy shit that worked.
                    
        else:  #note who doesn't have a genre
            no_genre_movie_list.append(row["title"])
            
print len(no_genre_movie_list)
# 68 movies have no genre. 
print genre_list

    
# want to make an new csv that is like the old csv,
# but has new columns for each genre, with a 0 or 1 
# for it the movie is not or is that genre respectively
    
    
    
genre_dict = {}

with open(csv_filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    temp_list = list(reader)
    for genre in genre_list:
        genre_dict[genre] = []
        for i, row in enumerate(temp_list):
            if i > 0:
                genres = re.findall('(\w+)', row["genre"])      
                if genre in genres:
                    (genre_dict[genre]).append(1)
                else:
                    (genre_dict[genre]).append(0)
                    
#print genre_dict        
  

"""
OK Nat.  I have made a dictionary, with each key (genre) giving a list of numbers corresponding to the list of movies 
in your csv.  They are ordered the same. 960 of them.   Now I need these dictionarys added as columns to the main csv. 

"""

   