import os
import sys

video_dir = 'F:\\582 videos\\video_files'
mp3_dir = 'F:\\582 videos\\mp3s'

def save_audio(full_pathname, filename):
    filename_stem = '.'.join(filename.split('.')[:-1])

    print "Converting %s to %s" % (full_pathname, os.path.join(mp3_dir, filename_stem + '.mp3'))
    os.system('ffmpeg -i "%s" "%s"' % (full_pathname, os.path.join(mp3_dir, filename_stem + '.mp3')))

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
                save_audio(os.path.join(dirname, filename), filename)

if __name__ == '__main__':
    main()