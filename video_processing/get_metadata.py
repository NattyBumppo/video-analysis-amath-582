import urllib2
import re
import sys
import time
import csv

movie_title_search_pattern = '<h1 itemprop="name">(.+)</h1>'
flv_file_search_pattern = 'src="(http://videos.movie-list.com/flvplayer.swf\?file=http://cdn.movie-list.com/flvideo/\S+.flv)"'
mov_file_search_pattern1 = 'HREF="(\S+\.mov)">'
mov_file_search_pattern2 = 'href="(\S+\.mov)">'
mp4_file_search_pattern = 'file: "(http://cdn.movie-list.com/hd/\S+.mp4)"'
genre_search_pattern = 'itemprop="genre">([A-Za-z0-9 ,]+)</span>'
release_date_search_pattern = 'Release Date: <span style="color:#181818; font-size:12px;">(.+)</span></span>'
imdb_search_pattern = 'href=[\'"](http:\/\/[w]*\.*imdb\.com\/title\/[A-Za-z0-9]+\/)[\'"]'
trailer_specific_file_search_pattern = 'Trailer</span>.*file: "(.*hd/.*?mp4)"'

# Grab URLs from file
urls_filename = 'urls.txt'

with open(urls_filename, 'r') as url_file:
    lines = url_file.readlines()

    # Set up a list of movies in which to put all of the movie data
    movie_list = []

    for i, line in enumerate(lines):
        # Set up a dictionary for each movie in which to store its data
        movie_dict = {}

        # Strip out surrounding whitespace to grab the url
        url = line.strip()

        print "Processing URL %s of %s (%s)" % (i, len(lines), url)
        
        # Grab the webpage data
        webpage_data = urllib2.urlopen(url).read()

        movie_dict['webpage_url'] = url

        # Use regexes to parse out lots of fun data
        movie_title_matches = re.findall(movie_title_search_pattern, webpage_data)
        if len(movie_title_matches) > 0:
            movie_dict['movie_title'] = movie_title_matches[0]

        flv_file_matches = re.findall(flv_file_search_pattern, webpage_data)
        if len(flv_file_matches) > 0:
            movie_dict['flv_files'] = flv_file_matches

        mov_file_matches1 = re.findall(mov_file_search_pattern1, webpage_data)
        if len(mov_file_matches1) > 0:
            movie_dict['mov1_files'] = mov_file_matches1

        mov_file_matches2 = re.findall(mov_file_search_pattern2, webpage_data)
        if len(mov_file_matches2) > 0:
            movie_dict['mov2_files'] = mov_file_matches2

        mp4_file_matches = re.findall(mp4_file_search_pattern, webpage_data)
        if len(mp4_file_matches) > 0:
            movie_dict['mp4_files'] = mp4_file_matches

        genre_matches = re.findall(genre_search_pattern, webpage_data)
        if len(genre_matches) > 0:
            movie_dict['genre'] = genre_matches[0]

        release_date_matches = re.findall(release_date_search_pattern, webpage_data)
        if len(release_date_matches) > 0:
            movie_dict['release_date'] = release_date_matches[0]

        imdb_url_matches = re.findall(imdb_search_pattern, webpage_data)
        if len(imdb_url_matches) > 0:
            movie_dict['imdb_url'] = imdb_url_matches[0]

        trailer_specific_file_match = re.findall(trailer_specific_file_search_pattern, webpage_data, re.DOTALL)
        if len(trailer_specific_file_match) > 0:
            movie_dict['trailer_specific_file'] = trailer_specific_file_match[0]

        if (len(mp4_file_matches) + len(mov_file_matches2) + len(mov_file_matches1) + len(flv_file_matches) == 0):
            # No videos found, so we'll skip adding this one to the dictionary
            pass
        else:
            # Store this dictionary in the list of movies
            movie_list.append(movie_dict)     

        # A sleep command just so the website doesn't think I'm DOSing it...
        time.sleep(0.3)

# Write movie list into a csv
possible_keys = ['movie_title', 'webpage_url', 'genre', 'release_date', 'imdb_url', 'flv_files', 'mov1_files', 'mov2_files', 'mp4_files', 'trailer_specific_file']
csv_filename = 'movies.csv'
with open(csv_filename, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(possible_keys)
    for movie in movie_list:
        # Make sure everything's in the right order...
        value_list = []
        for key in possible_keys:
            if key in movie:
                value_list.append(movie[key])
            else:
                # Blank cell
                value_list.append('')
        writer.writerow(value_list)