import csv
import unicodedata
import re
import sys

# Formats a title so that it can be used as a directory name
def format_title_for_file_system(movie_title):
    try:
        movie_title = unicodedata.normalize('NFKD', unicode(movie_title)).encode('ascii', 'ignore')
        movie_title = unicode(re.sub('[^\w\s-]', '', movie_title).strip())
        movie_title = unicode(re.sub('[-\s]+', '-', movie_title).strip())
        movie_title = str(movie_title)
    except UnicodeDecodeError:
        print "Error parsing movie title:", movie_title
        sys.exit()

    return movie_title

# Movie metadata csv file
csv_filename = 'movies.csv'
# File containing various metrics from video analysis
video_analysis_filename = 'video_analysis.txt'
audio_analysis_filename = 'audio_analysis.txt'

# File to hold all of the new, coalesced data
final_csv_filename = 'trailer_data.csv'

# First, let's ingest the video analysis file into a dictionary
analysis_dict = {}

with open(video_analysis_filename, 'r') as analysis_file:
    lines = analysis_file.readlines()

while (len(lines) > 7):
    # Get the lines for a single movie
    movie_lines = lines[:7]

    # Parse data
    title = movie_lines[0].split(':')[-1].strip()
    num_frames = int(movie_lines[1].split(':')[-1])
    total_time = float(movie_lines[2].split(':')[-1])
    avg_intensity = float(movie_lines[3].split(':')[-1])
    avg_color_r = float(movie_lines[4].split(':')[-1].strip().split(' ')[0])
    avg_color_g = float(movie_lines[4].split(':')[-1].strip().split(' ')[1])
    avg_color_b = float(movie_lines[4].split(':')[-1].strip().split(' ')[2])
    avg_shot_length = float(movie_lines[5].split(':')[-1])
    num_shots = int(movie_lines[6].split(':')[-1])

    # Make a dictionary for just this movie
    movie_dict = {}
    movie_dict['title'] = title
    movie_dict['num_frames'] = num_frames
    movie_dict['total_time'] = total_time
    movie_dict['avg_intensity'] = avg_intensity    
    movie_dict['avg_color_r'] = avg_color_r
    movie_dict['avg_color_g'] = avg_color_g
    movie_dict['avg_color_b'] = avg_color_b
    movie_dict['avg_shot_length'] = avg_shot_length
    movie_dict['num_shots'] = num_shots

    # Add this dictionary to the dictionary of all movies
    analysis_dict[title] = movie_dict

    # Remove this movie (and the trailing blank line) from our list
    lines = lines[8:]
    
with open(audio_analysis_filename, 'r') as analysis_file:
    lines = analysis_file.readlines()

while (len(lines) > 5):
    # Get the lines for a single movie
    movie_lines = lines[:5]

    # Parse data
    title = movie_lines[0].split(':')[-1].strip()
    mean_volume = float(movie_lines[1].split(':')[-1].strip())
    std_dev_volume = float(movie_lines[2].split(':')[-1].strip())
    min_volume = float(movie_lines[3].split(':')[-1].strip())
    max_volume = float(movie_lines[4].split(':')[-1].strip())

    # Make a dictionary for just this movie
    movie_dict = {}
    movie_dict['title'] = title
    movie_dict['mean_volume'] = mean_volume
    movie_dict['std_dev_volume'] = std_dev_volume
    movie_dict['min_volume'] = min_volume
    movie_dict['max_volume'] = max_volume

    # Add this dictionary to the dictionary of all movies
    if title in analysis_dict:
        for key in movie_dict.keys():
            # Add everything to the analysis_dict entry for this movie...
            # except for the title, which has already been added!
            if key != 'title':
                analysis_dict[title]['mean_volume'] = mean_volume
                analysis_dict[title]['std_dev_volume'] = std_dev_volume
                analysis_dict[title]['min_volume'] = min_volume
                analysis_dict[title]['max_volume'] = max_volume
    else:
        analysis_dict[title] = movie_dict

    # Remove this movie (and the trailing blank line) from our list
    lines = lines[6:]

# Now, we've accumulated a dictionary of all of the movies!
# Next, let's read in the old metadata csv file
with open(csv_filename, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        # Parse out the data for each movie
        nice_title = row['movie_title']
        webpage_url = row['webpage_url']
        genre = row['genre']
        release_date = row['release_date']
        imdb_url = row['imdb_url']

        # Now, we'll get the version of the "nicely formatted title" that will
        # match the version we pulled from the other file
        not_as_nice_title = format_title_for_file_system(nice_title)

        # Now, we'll check to see if we match anything in the analysis dictionary,
        # and if so, we'll add to it!
        if not_as_nice_title in analysis_dict:
            # A match! Let's add our data for this movie...
            analysis_dict[not_as_nice_title]['original_format_title'] = nice_title
            analysis_dict[not_as_nice_title]['movie_list_webpage_url'] = webpage_url
            analysis_dict[not_as_nice_title]['genre'] = genre
            analysis_dict[not_as_nice_title]['release_date'] = release_date
            analysis_dict[not_as_nice_title]['imdb_url'] = imdb_url

# # Print out some test data
# print analysis_dict[analysis_dict.keys()[0]]
# print analysis_dict[analysis_dict.keys()[1]]
# print analysis_dict[analysis_dict.keys()[2]]

# Now, dump everything into a new .csv file!
with open(final_csv_filename, 'wb') as csv_file:
    fieldnames = ['title', 'num_frames', 'total_time', 'avg_intensity', 'avg_color_r', 'avg_color_g', 'avg_color_b', 'avg_shot_length', 'num_shots', 'original_format_title', 'movie_list_webpage_url', 'genre', 'release_date', 'imdb_url', 'mean_volume', 'std_dev_volume', 'min_volume', 'max_volume']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for key in analysis_dict.keys():
        writer.writerow(analysis_dict[key])