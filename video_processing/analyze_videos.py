import cv2
import os
import sys
import numpy as np
import csv

# Get a frame from the current video source
def getFrame(cap):
    _, frame = cap.read()
    return frame

def analyze_video(filename):
    print 'Analyzing', filename

    # Get a camera input source
    cap = cv2.VideoCapture(filename)

    fps = cap.get(cv2.CAP_PROP_FPS)

    frameNo = 0
    
    avg_colors = []

    shot_transition_threshold = 100000
    shot_transitions = [0.0]

    dark_threshold = 5
    dark_frame_count = 0

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

        else:
            # Dark frame; skip on our averaging
            dark_frame_count += 1
            pass

        # Accumulate this frame's pixels
        frame_accumulator = np.add(frame_accumulator, frame)

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

    # Now that we have an accumulated image, let's add together ALL of the pixels
    accumulated_color_sum = np.sum(np.sum(frame_accumulator, 1), 0)

    print 'accumulated_color_sum:', accumulated_color_sum

    # Divide by the number of non-dark frames to get the average pixel sum for a frame
    avg_pixel_sum = np.true_divide(accumulated_color_sum, frameNo - dark_frame_count)

    print 'avg_pixel_sum:', avg_pixel_sum

    # Now, we just need to divide by the number of non-zero pixels (the pixels that are zero
    # are probably letterbox pixels, and we should ignore them. (The np.all() below reduces
    # the three RGB elements to just a single element, true when R, G, and B are all greater
    # than the dark_threshold and false otherwise.)
    num_pixels = np.sum(np.all(np.greater(frame_accumulator, dark_threshold), 2))

    print 'num_pixels:', num_pixels
    
    avg_color = np.true_divide(avg_pixel_sum, num_pixels).tolist()

    print 'avg_color:', avg_color

    # Convert to grayscale intensity using standard weights
    avg_intensity = avg_color[0] * 0.2989 + avg_color[1] * 0.5870 + avg_color[2] * 0.1140

    print 'avg_intensity:', avg_intensity

    # Get various transition time-related data items
    shot_lengths = [j-i for i, j in zip(shot_transitions[:-1], shot_transitions[1:])]
    avg_shot_length = sum(shot_lengths) / float(len(shot_lengths))
    num_shots = len(shot_lengths)

    return frameNo, current_time, avg_intensity, avg_color, avg_shot_length, num_shots

def main():
    video_dir = 'video_files'

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
                    num_frames, total_time, avg_intensity, avg_color, avg_shot_length, num_shots = analyze_video(os.path.join(dirname, filename))

                    print 'Movie title:', movie_title
                    print 'Number of frames:', num_frames
                    print 'Total time (s):', total_time
                    print 'Average Pixel Intensity', avg_intensity
                    print 'Average Pixel Color:', avg_color
                    print 'Average Shot Length (s):', avg_shot_length
                    print 'Number of Shots:', num_shots

                    # Open file in which to log all of this data
                    with open('video_analysis.txt', 'a') as outfile:

                        # Output this data
                        outfile.write('movie_title: ' + movie_title + '\n')
                        outfile.write('num_frames: ' + str(num_frames) + '\n')
                        outfile.write('total_time: ' + str(total_time) + '\n')
                        outfile.write('avg_intensity: ' + str(avg_intensity) + '\n')
                        outfile.write('avg_color: ' + str(avg_color) + '\n')
                        outfile.write('avg_shot_length: ' + str(avg_shot_length) + '\n')
                        outfile.write('num_shots: ' + str(num_shots) + '\n\n')

if __name__ == '__main__':
    main()