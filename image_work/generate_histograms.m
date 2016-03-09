% Initial cleanup
clear; close all; clc;

input_video = 'F:\582 videos\video_files\Frozen-Fever\frozenfever720.mp4';
shot_transition_frame = 406;

% Load video and get images from just before the shot and just after
video_object = VideoReader(input_video);

% We'll grab three shots--two right before the transition, and two right
% after the transition
frame1 = read(video_object, shot_transition_frame - 8);
frame2 = read(video_object, shot_transition_frame - 4);
frame3 = read(video_object, shot_transition_frame + 4);

% Now, display each of these frames (I'll save them to make them into a
% neato image in another program)
figure(1);
imshow(frame1);
figure(2);
imshow(frame2);
figure(3);
imshow(frame3);

% Now, let's draw the color histograms for each frame
figure(4);
frame_r = frame1(:,:,1);
frame_g = frame1(:,:,2);
frame_b = frame1(:,:,3);

[yRed, x] = imhist(frame_r);
[yGreen, x] = imhist(frame_g);
[yBlue, x] = imhist(frame_b);

plot(x, yRed, 'Red', x, yGreen, 'Green', x, yBlue, 'Blue');
axis([0 270 0 15000]);
title('Frame 1 Color Histogram (Pre-Shot Transition)');
xlabel('Color Intensity (RGB)');
ylabel('Histogram Bin Count');

figure(5);
frame_r = frame2(:,:,1);
frame_g = frame2(:,:,2);
frame_b = frame2(:,:,3);

[yRed, x] = imhist(frame_r);
[yGreen, x] = imhist(frame_g);
[yBlue, x] = imhist(frame_b);

plot(x, yRed, 'Red', x, yGreen, 'Green', x, yBlue, 'Blue');
axis([0 270 0 15000]);
title('Frame 2 Color Histogram (Pre-Shot Transition)');
xlabel('Color Intensity (RGB)');
ylabel('Histogram Bin Count');

figure(6);
frame_r = frame3(:,:,1);
frame_g = frame3(:,:,2);
frame_b = frame3(:,:,3);

[yRed, x] = imhist(frame_r);
[yGreen, x] = imhist(frame_g);
[yBlue, x] = imhist(frame_b);

plot(x, yRed, 'Red', x, yGreen, 'Green', x, yBlue, 'Blue');
axis([0 270 0 15000]);
title('Frame 3 Color Histogram (Post-Shot Transition)');
xlabel('Color Intensity (RGB)');
ylabel('Histogram Bin Count');