% Initial cleanup
clear; close all; clc;

infilename = 'more_trailer_dataNOCOMMA_w_octave.csv';
outfilename = 'more_trailer_dataNOCOMMA_w_octave_standardized.csv';

% Load csv
delimiter = ',';
startRowOffset = 1;

% Note that I'm skipping the first column (which is text). This makes
% things a little easier for me in terms of loading the .csv, but this
% laziness on my part means that when I generate the output .csv, I'll be
% making a file without the movie titles. I'll add them back with a
% copy-and-paste job as the last, manual step. It's less work than
% processing it in such a way that I save this data...
startColOffset = 1;
data = csvread(infilename, startRowOffset, startColOffset);

% We'll also cut out all of the binary genre identifiers...
data = data(:, 1:41);

numRows = size(data, 1);

% Now, take each column, subtract its mean, and divide by the std dev
means = repmat(mean(data, 1), numRows, 1);
stddevs = repmat(std(data, 0, 1), numRows, 1);
standardized_data = (data - means) ./ stddevs;

% Now export that shizzy
csvwrite(outfilename, standardized_data);