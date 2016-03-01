import os
import sys

video_dir = 'C:\\Users\\Noel_K\\git_repository\\video-analysis-amath-582\\video_processing\\video_files'
mp3_dir = 'C:\\Users\\Noel_K\\git_repository\\video-analysis-amath-582\\video_processing\\mp3s'

def save_audio(full_pathname, movie_title, filename):
    filename_stem = '.'.join(filename.split('.')[:-1])

    print "Converting %s to %s" % (full_pathname, os.path.join(mp3_dir, filename_stem + '.mp3'))
    os.system('C:\\ffmpeg\\bin\\ffmpeg.exe -i "%s" "%s"' % (full_pathname, os.path.join(mp3_dir, movie_title + '.mp3')))

def main():
    # Go through all directories
    for dirname, dirnames, filenames in os.walk(video_dir):
        # print dirname
        # print dirnames
        # print filenames
        # print '---'

        # Only look at non-empty directories
        if len(filenames) > 0:
            for filename in filenames:
                movie_title = dirname.split('\\')[-1]
                save_audio(os.path.join(dirname, filename), movie_title, filename)

if __name__ == '__main__':
    main()