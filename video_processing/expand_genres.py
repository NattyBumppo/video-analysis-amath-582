# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 14:30:50 2016

@author: fuini
"""


import csv
import re

csv_filename = "trailer_data.csv"

my_dict = {}

# list of my genres
no_genre_movie_list = []
genre_list = []
genre_count = {}

#findin the genres and the movies without genres
with open(csv_filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for i, row in enumerate(reader):
        if row["genre"]:
            # build genre list being all regexy like Nat
            genres = re.findall('(\w+)', row["genre"])
            for genre in genres:
                if genre in genre_list:
                    genre_count[genre] += 1
                else:
                    genre_list.append(genre)
                    genre_count[genre] = 1
                    
            # holy shit that worked.
                    
        else:  #note who doesn't have a genre
            no_genre_movie_list.append(row["title"])
            
print "Number of movies with no genre: " + str(len(no_genre_movie_list))
# 68 movies have no genre. 
print "Number of unique genres: " + str(len(genre_list))
print genre_list
# 25 genres
print "Each genre and number of times present in data: "
print genre_count
print "We should seriously consider removing genres that have only a few representatives, as we don't have the statistics to say anything meaningful."



#Read in and save CSV into my_dict, while building new rows into my_dict
with open(csv_filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for i, row in enumerate(reader):
        my_dict[row["title"]] = {}
        for key in row.keys():            
            my_dict[row["title"]][key] = row[key]
            #collect genres of movie
            genres_of_movie = re.findall('(\w+)', row["genre"])
            #loop through all genres, append 0 or 1 for each genre
            for genre in genre_list: 
                if genre in genres_of_movie:
                    my_dict[row["title"]][genre] = 1
                else:
                    my_dict[row["title"]][genre] = 0
        # check genre business
        # loop over my list of genres
print my_dict["Step-Up-All-In"]


#now write out my dict to a csv
final_csv_filename = "trailer_data_expanded_genre.csv"
with open(final_csv_filename, 'wb') as csv_file:
    fieldnames = ['title', 'num_frames', 'total_time', 'avg_intensity', 'avg_color_r', 'avg_color_g', 'avg_color_b', 'avg_shot_length', 'num_shots', 'original_format_title', 'movie_list_webpage_url', 'genre', 'release_date', 'imdb_url', 'mean_volume', 'std_dev_volume', 'min_volume', 'max_volume', 'Drama', 'Horror', 'Thriller', 'Action', 'Comedy', 'Crime', 'Mystery', 'Sport', 'Romance', 'Biography', 'History', 'Animation', 'Adventure', 'Family', 'Documentary', 'Fantasy', 'Music', 'Western', 'Musical', 'Sports', 'Supernatural', 'War', 'News', 'Animaton', 'Short']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for key in my_dict.keys():
        writer.writerow(my_dict[key])

