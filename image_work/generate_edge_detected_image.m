% Initial cleanup
clear; close all; clc;

input_video1 = 'F:\582 videos\video_files\Kung-Fu-Panda-3\kungfupanda3720.mp4';
input_video1_edge_detection_frame = 2160;

input_video2 = 'F:\582 videos\video_files\Interstellar\interstellar720.mp4';
input_video2_edge_detection_frame = 2208;

% Load videos and get frames
video_object1 = VideoReader(input_video1);
video_object2 = VideoReader(input_video2);

frame1 = read(video_object1, input_video1_edge_detection_frame);
frame2 = read(video_object2, input_video2_edge_detection_frame);

% Now, display each of these frames (I'll save them to make them into a
% neato image in another program)
figure(1);
imshow(frame1);
figure(2);
imshow(frame2);

% Now, perform Canny edge detection on each frame (need to convert to
% black-and-white first)
frame1 = rgb2gray(frame1);
frame2 = rgb2gray(frame2);
edge1 = edge(frame1, 'Canny');
edge2 = edge(frame2, 'Canny');

% And display!
figure(3);
imshow(edge1);
figure(4);
imshow(edge2);