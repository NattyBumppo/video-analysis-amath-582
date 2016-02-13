import cv2
import os


# Get a frame from the current video source
def getFrame(cap):
    _, frame = cap.read()
    return frame

def analyze_video(filename):
    print 'Analyzing', filename

    # Get a camera input source
    cap = cv2.VideoCapture(filename)

    frameNo = 0

    avg_colors = []

    while(cap.isOpened()):
        frame = getFrame(cap)
        if frame is None:
            break
        # Makes a copy before any changes occur
        # frameCopy = frame.copy()

        frameNo += 1

        # Get the average color for this frame
        avg_color = cv2.mean(frame)[:3]
        avg_colors.append(avg_color)


    # Average together all of the avg_colors
    avg_color = [sum(color_channel) / float(len(color_channel)) for color_channel in zip(*avg_colors)]

    # Convert to grayscale intensity using standard weights
    avg_intensity = avg_color[0] * 0.2989 + avg_color[1] * 0.5870 + avg_color[2] * 0.1140

    return frameNo, avg_intensity, avg_color, 0

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
                num_frames, avg_intensity, avg_color, avg_cut_length = analyze_video(os.path.join(dirname, filename))

                print 'num_frames:', num_frames
                print 'avg_intensity:', avg_intensity
                print 'avg_color:', avg_color
                print 'avg_cut_length:', avg_cut_length


if __name__ == '__main__':
    main()