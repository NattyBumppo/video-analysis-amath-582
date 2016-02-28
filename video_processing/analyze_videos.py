import cv2
import os
import sys
import numpy as np
import csv
from moviepy.editor import VideoFileClip, AudioClip

video_analysis_mode = True
video_dir = 'F:\\582 videos\\test_vids'

if video_analysis_mode:
    analysis_results_file = 'video_analysis.txt'
else:
    analysis_results_file = 'audio_analysis.txt'

# Get a frame from the current video source
def getFrame(cap):
    _, frame = cap.read()
    return frame

def is_video_already_analyzed(movie_title):
    # print movie_title
    # Check in the file and make sure we don't already have an entry for this
    # with open('video_analysis.txt', 'r') as infile:
    with open(analysis_results_file, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            if 'movie_title: ' + str(movie_title) in line:
                return True
            else:
                pass
        return False

# Get the sound amplitude statistics for the video
# (mean, standard deviation, max, and minimum)
def analyze_sound(filename):
    print 'Analyzing audio for', filename

    # Load video file
    clip = VideoFileClip(filename)

    # Make a lambda function for breaking a video clip into sound arrays
    cut = lambda i: clip.audio.subclip(i, i+1).to_soundarray(fps=44100, nbytes=4)

    # Make a lambda function for grabbing the volume of a sound array
    volume = lambda array: np.sqrt(((1.0*array)**2).mean())
    # Grab the volumes for this video file
    volumes = [volume(cut(i)) for i in range(0, int(clip.duration-1))]

    volumes_std_floats = [float(vol) for vol in volumes]
    volumes_strings = ["%.2f" % vol for vol in volumes_std_floats]

    volume_mean = np.mean(volumes)
    volume_std_dev = np.std(volumes)
    volume_min = np.min(volumes)
    volume_max = np.max(volumes)

    # Get rid of super-small mins
    epsilon = 0.001
    if volume_min < epsilon:
        volume_min = 0.0

    return float(volume_mean), float(volume_std_dev), float(volume_min), float(volume_max), volumes_strings

# Get video-related characteristics for the video
def analyze_video(filename):
    print 'Analyzing video for', filename

    # Get a camera input source
    cap = cv2.VideoCapture(filename)

    fps = cap.get(cv2.CAP_PROP_FPS)

    frameNo = 0
    
    avg_colors = []

    shot_transition_threshold = 100000
    shot_transitions = [0.0]

    dark_threshold = 5
    consecutive_dark_frame_count = 0
    # This will be a list of all of the "dark scenes," by frame count
    dark_scene_list = []

    # List for average colors
    avg_color_list = []

    while(cap.isOpened()):
        frame = getFrame(cap)
        if frame is None:
            break

        height, width = frame.shape[:2]
        dimensional_ratio = float(width) / float(height)

        # Initialize frame accumulator, if necessary
        if frameNo == 0:
            frame_accumulator = np.zeros((height, width, 3), np.uint64)

        current_time = float(frameNo) / float(fps)

        # Check to make sure this isn't a fully black frame (if it is, averaging it
        # into the other colors will throw us off)
        if not np.all(np.less(frame, dark_threshold)):
            # # Get the average color for this frame
            # avg_color = cv2.mean(frame)[:3]
            # avg_colors.append(avg_color)

            # Accumulate this frame's pixels
            frame_accumulator = np.add(frame_accumulator, frame)

            # If this was the end of a "dark scene" (i.e., a dark transition),
            # then let's dump the current dark frame count into the dark scene
            # list and reset the count
            if consecutive_dark_frame_count > 0:
                dark_scene_list.append(consecutive_dark_frame_count)
                consecutive_dark_frame_count = 0

            # Debug prints for color debugging
            avg_color_this_frame = cv2.mean(frame)[:3]
            avg_color_list.append(avg_color_this_frame)
            # avg_intensity_this_frame = float(avg_color_this_frame[0] * 0.2989 + avg_color_this_frame[1] * 0.5870 + avg_color_this_frame[2] * 0.1140)
            # print frameNo, avg_intensity_this_frame
            # if avg_intensity_this_frame < 5.0:
            #     print frame


        else:
            # Dark frame; skip on our averaging
            # print "dark frame"
            consecutive_dark_frame_count += 1

        # Calculate the color histogram for this frame and compare to the previous one
        # (if the chi-squared distance between the two histograms exceeds the shot
        # transition threshold, then we'll assume we've experienced a transition)
        current_frame_histogram = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        if frameNo != 0:
            chi_squared_distance = cv2.compareHist(current_frame_histogram, previous_frame_histogram, cv2.HISTCMP_CHISQR)
            # print frameNo, chi_squared_distance
            if chi_squared_distance > shot_transition_threshold:
                # Shot transition detected! We'll record the current time in seconds
                shot_transitions.append(current_time)

        previous_frame_histogram = current_frame_histogram

        frameNo += 1


    # If this was the end of a "dark scene" (i.e., a dark transition),
    # then let's dump the current dark frame count into the dark scene list
    if consecutive_dark_frame_count > 0:
        dark_scene_list.append(consecutive_dark_frame_count)

    # Now that we have an accumulated image, let's add together ALL of the pixels
    accumulated_color_sum = np.sum(np.sum(frame_accumulator, 1), 0)

    print 'accumulated_color_sum:', accumulated_color_sum

    # Divide by the number of non-dark frames to get the average pixel sum for a frame
    avg_pixel_sum = np.true_divide(accumulated_color_sum, frameNo - sum(dark_scene_list))

    print 'avg_pixel_sum:', avg_pixel_sum

    # Now, we just need to divide by the number of non-zero pixels (the pixels that are zero
    # are probably letterbox pixels, and we should ignore them. (The np.all() below reduces
    # the three RGB elements to just a single element, true when R, G, and B are all greater
    # than the dark_threshold and false otherwise.)
    num_pixels = np.sum(np.all(np.greater(frame_accumulator, dark_threshold), 2))

    print 'num_pixels:', num_pixels
    
    avg_color = np.true_divide(avg_pixel_sum, num_pixels).tolist()

    print 'avg_color:', avg_color

    # Do a few calculations that tell us about color distribution, although they don't
    # take into account the presence of a letterbox (too much of a pain in the butt this way)
    avg_color_with_letterbox = np.mean(avg_color_list, 0)
    stddev_color_with_letterbox = np.std(avg_color_list, 0)
    min_color_with_letterbox = np.min(avg_color_list, 0)
    max_color_with_letterbox = np.max(avg_color_list, 0)

    print "Mean of color without removing letterbox", avg_color_with_letterbox.tolist()
    print "Standard deviation of color without removing letterbox", stddev_color_with_letterbox.tolist()
    print "Min of color without removing letterbox", min_color_with_letterbox.tolist()
    print "Max of color without removing letterbox", max_color_with_letterbox.tolist()

    # Convert to grayscale intensity using standard weights
    avg_intensity = avg_color[0] * 0.2989 + avg_color[1] * 0.5870 + avg_color[2] * 0.1140

    print 'avg_intensity:', avg_intensity

    # Get various transition time-related data items
    shot_lengths = [j-i for i, j in zip(shot_transitions[:-1], shot_transitions[1:])]
    avg_shot_length = sum(shot_lengths) / float(len(shot_lengths))
    num_shots = len(shot_lengths)

    # Calculate data related to consecutive dark frames (pitch black transitions, a.k.a. dark scenes)
    print "dark scene data:", dark_scene_list
    dark_scene_mean_length = float(np.mean(dark_scene_list))
    dark_scene_length_std_dev = float(np.std(dark_scene_list))
    dark_scene_length_max = float(np.max(dark_scene_list))
    dark_scene_length_min = float(np.min(dark_scene_list))
    dark_scene_count = len(dark_scene_list)
    dark_scene_percentage = float(dark_scene_count) / float(frameNo)

    print 'dark_scene_mean_length:', dark_scene_mean_length
    print 'dark_scene_length_std_dev:', dark_scene_length_std_dev
    print 'dark_scene_length_max:', dark_scene_length_max
    print 'dark_scene_length_min:', dark_scene_length_min
    print 'dark_scene_count:', dark_scene_count
    print 'dark_scene_percentage:', dark_scene_percentage

    return frameNo, current_time, avg_intensity, avg_color, avg_shot_length, num_shots, stddev_color_with_letterbox, dark_scene_mean_length, dark_scene_length_std_dev, dark_scene_length_max, dark_scene_length_min, dark_scene_count, dark_scene_percentage

def main():
    # Create video analysis (or audio analysis) results file, in case it doesn't already exist
    open(analysis_results_file, 'a').close()

    # Go through all directories
    for dirname, dirnames, filenames in os.walk(video_dir):
        # print dirname
        # print dirnames
        # print filenames
        # print '---'

            # Only look at non-empty directories
            if len(filenames) > 0:
                for filename in filenames:
                    # Parse out the movie name from the directory name
                    movie_title = dirname.split('\\')[-1]

                    if is_video_already_analyzed(movie_title):
                        print "%s already analyzed; skipping" % movie_title
                        continue
                    else:
                        if video_analysis_mode:
                            num_frames, total_time, avg_intensity, avg_color, avg_shot_length, num_shots, stddev_color_with_letterbox, dark_scene_mean_length, dark_scene_length_std_dev, dark_scene_length_max, dark_scene_length_min, dark_scene_count, dark_scene_percentage = analyze_video(os.path.join(dirname, filename))
                        else:
                            mean_volume, std_dev_volume, min_volume, max_volume, volumes_strings = analyze_sound(os.path.join(dirname, filename))

                    print 'Movie title:', movie_title

                    if video_analysis_mode:
                        print 'Number of frames:', num_frames
                        print 'Total time (s):', total_time
                        print 'Average Pixel Intensity', avg_intensity
                        print 'Average Pixel Color:', avg_color
                        print 'Average Shot Length (s):', avg_shot_length
                        print 'Number of Shots:', num_shots
                        print 'Standard deviation of color (with letterbox):', stddev_color_with_letterbox
                        print 'Mean length of transitional black scenes:', dark_scene_mean_length
                        print 'Standard deviation of length of transitional black scenes:', dark_scene_length_std_dev
                        print 'Max length of transitional black scenes:', dark_scene_length_max
                        print 'Min length of transitional black scenes:', dark_scene_length_min
                        print 'Total count of transitional black scenes:', dark_scene_count
                        print 'Percentage of trailer occupied by transitional black scene frames:', dark_scene_percentage
                    else:
                        print 'Mean Volume:', mean_volume
                        print 'Volume Standard Deviation:', std_dev_volume
                        print 'Minimum Volume', min_volume
                        print 'Maximum Volume', max_volume
                        print 'Volumes Strings', volumes_strings

                    # Open file in which to log all of this data
                    with open(analysis_results_file, 'ab') as outfile:
                        # Output this data
                        outfile.write('movie_title: ' + movie_title + '\n')

                        if video_analysis_mode:
                            # Output video analysis metrics
                            outfile.write('num_frames: ' + str(num_frames) + '\n')
                            outfile.write('total_time: ' + str(total_time) + '\n')
                            outfile.write('avg_intensity: ' + str(avg_intensity) + '\n')
                            outfile.write('avg_color: ' + str(avg_color) + '\n')
                            outfile.write('avg_shot_length: ' + str(avg_shot_length) + '\n')
                            outfile.write('num_shots: ' + str(num_shots) + '\n\n')
                            outfile.write('stddev_color_with_letterbox: ' + str(stddev_color_with_letterbox) + '\n\n')
                            outfile.write('dark_scene_mean_length: ' + str(dark_scene_mean_length) + '\n\n')
                            outfile.write('dark_scene_length_std_dev: ' + str(dark_scene_length_std_dev) + '\n\n')
                            outfile.write('dark_scene_length_max: ' + str(dark_scene_length_max) + '\n\n')
                            outfile.write('dark_scene_length_min: ' + str(dark_scene_length_min) + '\n\n')
                            outfile.write('dark_scene_count: ' + str(dark_scene_count) + '\n\n')
                            outfile.write('dark_scene_percentage: ' + str(dark_scene_percentage) + '\n\n')
                        else:
                            # Output audio analysis metrics
                            outfile.write('mean_volume: ' + str(mean_volume) + '\n')
                            outfile.write('std_dev_volume: ' + str(std_dev_volume) + '\n')
                            outfile.write('min_volume: ' + str(min_volume) + '\n')
                            outfile.write('max_volume: ' + str(max_volume) + '\n\n')



if __name__ == '__main__':
    main()