import os
import sys
from pydub import AudioSegment
AudioSegment.converter = r"C:\\ffmpeg\\bin\\ffmpeg.exe"

mp3_dir = 'C:\\Users\\Noel_K\\git_repository\\video-analysis-amath-582\\video_processing\\mp3s'
clipped_mp3_dir = 'C:\\Users\\Noel_K\\git_repository\\video-analysis-amath-582\\video_processing\\clipped'

clip_size_ms = 10000

def clip_and_save_audio(full_pathname, filename):

    sound = AudioSegment.from_mp3(full_pathname)

    # len() and slicing are in milliseconds
    halfway_point = len(sound) / 2
    start_point = halfway_point - clip_size_ms / 2
    stop_point = halfway_point + clip_size_ms / 2
    clip_samples = sound[start_point:stop_point]

    filename_stem = '.'.join(filename.split('.')[:-1])
    print "Saving %s as %s" % (full_pathname, os.path.join(clipped_mp3_dir, filename_stem + '.mp3'))

    clip_samples.export(os.path.join(clipped_mp3_dir, filename_stem + '.mp3'), format="mp3")

    print full_pathname

def main():
    # Go through all directories
    for dirname, dirnames, filenames in os.walk(mp3_dir):
        # print dirname
        # print dirnames
        # print filenames
        # print '---'

        # Only look at non-empty directories
        if len(filenames) > 0:
            for filename in filenames:
                clip_and_save_audio(os.path.join(dirname, filename), filename)

if __name__ == '__main__':
    main()