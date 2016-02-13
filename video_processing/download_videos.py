import urllib
import csv
import sys
import os
import time

def download_video(url, movie_title):
    print "Downloading trailer at %s (%s)" % (url, movie_title)

    video_directory = 'video_files'

    # Get filename
    filename = url.split('/')[-1]

    if not os.path.exists(video_directory + '/' + movie_title):
        os.makedirs(video_directory + '/' + movie_title)

    # Open the url and download into the movie directory
    try:
        urllib.urlretrieve(url, video_directory + '/' movie_title + '/' + filename)

    # Handle errors
    except Exception as e:
        print "Error: ", e, url

# Open .csv file
csv_filename = 'movies.csv'
with open(csv_filename, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Only download if there's an .mp4 file available
        if row['trailer_specific_file']:
            # Take the first available URL
            video_url = row['trailer_specific_file']

            # Grab the movie title, too
            title = row['movie_title']

            # Download!
            download_video(video_url, title)

    # Introduce just a little bit of delay, so we're not spamming
    # the server *quite* so much
    time.sleep(1)