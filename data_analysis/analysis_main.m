
%% Initialize variables.
filename = 'C:\Users\The Hollowed\Dropbox\MATLAB\Assignments\Final Project\Analysis\more_trailer_data.csv';
delimiter = ',';

%% Read columns of data as strings:
% For more information, see the TEXTSCAN documentation.
formatSpec = '%*s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%*s%*s%*s%*s%*s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter,  'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Convert the contents of columns containing numeric strings to numbers.
% Replace non-numeric strings with NaN.
raw = repmat({''},length(dataArray{1}),length(dataArray)-1);
for col=1:length(dataArray)-1
    raw(1:length(dataArray{col}),col) = dataArray{col};
end
numericData = NaN(size(dataArray{1},1),size(dataArray,2));

for col=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55]
    % Converts strings in the input cell array to numbers. Replaced non-numeric
    % strings with NaN.
    rawData = dataArray{col};
    for row=1:size(rawData, 1);
        % Create a regular expression to detect and remove non-numeric prefixes and
        % suffixes.
        regexstr = '(?<prefix>.*?)(?<numbers>([-]*(\d+[\,]*)+[\.]{0,1}\d*[eEdD]{0,1}[-+]*\d*[i]{0,1})|([-]*(\d+[\,]*)*[\.]{1,1}\d+[eEdD]{0,1}[-+]*\d*[i]{0,1}))(?<suffix>.*)';
        try
            result = regexp(rawData{row}, regexstr, 'names');
            numbers = result.numbers;
            
            % Detected commas in non-thousand locations.
            invalidThousandsSeparator = false;
            if any(numbers==',');
                thousandsRegExp = '^\d+?(\,\d{3})*\.{0,1}\d*$';
                if isempty(regexp(thousandsRegExp, ',', 'once'));
                    numbers = NaN;
                    invalidThousandsSeparator = true;
                end
            end
            % Convert numeric strings to numbers.
            if ~invalidThousandsSeparator;
                numbers = textscan(strrep(numbers, ',', ''), '%f');
                numericData(row, col) = numbers{1};
                raw{row, col} = numbers{1};
            end
        catch me
        end
    end
end


%% Exclude rows with non-numeric cells
I = ~all(cellfun(@(x) (isnumeric(x) || islogical(x)) && ~isnan(x),raw),2); % Find rows with non-numeric cells
raw(I,:) = [];

%% Allocate imported array to column variable names
num_frames = cell2mat(raw(:, 1));
total_time = cell2mat(raw(:, 2));
avg_intensity = cell2mat(raw(:, 3));
avg_color_r = cell2mat(raw(:, 4));
avg_color_g = cell2mat(raw(:, 5));
avg_color_b = cell2mat(raw(:, 6));
mean_shot_length = cell2mat(raw(:, 7));
std_dev_shot_length = cell2mat(raw(:, 8));
max_shot_length = cell2mat(raw(:, 9));
min_shot_length = cell2mat(raw(:, 10));
num_shots = cell2mat(raw(:, 11));
stddev_color_with_letterbox_r = cell2mat(raw(:, 12));
stddev_color_with_letterbox_g = cell2mat(raw(:, 13));
stddev_color_with_letterbox_b = cell2mat(raw(:, 14));
detail_score_mean = cell2mat(raw(:, 15));
detail_score_std_dev = cell2mat(raw(:, 16));
detail_score_max = cell2mat(raw(:, 17));
detail_score_min = cell2mat(raw(:, 18));
dark_scene_mean_length = cell2mat(raw(:, 19));
dark_scene_length_std_dev = cell2mat(raw(:, 20));
dark_scene_length_max = cell2mat(raw(:, 21));
dark_scene_length_min = cell2mat(raw(:, 22));
dark_scene_count = cell2mat(raw(:, 23));
dark_scene_percentage = cell2mat(raw(:, 24));
mean_volume = cell2mat(raw(:, 25));
std_dev_volume = cell2mat(raw(:, 26));
min_volume = cell2mat(raw(:, 27));
max_volume = cell2mat(raw(:, 28));
sudden_rise_count_per_cut = cell2mat(raw(:, 29));
sudden_fall_count_per_cut = cell2mat(raw(:, 30));
Drama = cell2mat(raw(:, 31));
Horror = cell2mat(raw(:, 32));
Thriller = cell2mat(raw(:, 33));
Action = cell2mat(raw(:, 34));
Comedy = cell2mat(raw(:, 35));
Crime = cell2mat(raw(:, 36));
Mystery = cell2mat(raw(:, 37));
Sport = cell2mat(raw(:, 38));
Romance = cell2mat(raw(:, 39));
Biography = cell2mat(raw(:, 40));
History = cell2mat(raw(:, 41));
Animation = cell2mat(raw(:, 42));
Adventure = cell2mat(raw(:, 43));
Family = cell2mat(raw(:, 44));
Documentary = cell2mat(raw(:, 45));
Fantasy = cell2mat(raw(:, 46));
Music = cell2mat(raw(:, 47));
Western = cell2mat(raw(:, 48));
Musical = cell2mat(raw(:, 49));
Sports = cell2mat(raw(:, 50));
Supernatural = cell2mat(raw(:, 51));
War = cell2mat(raw(:, 52));
News = cell2mat(raw(:, 53));
Animaton = cell2mat(raw(:, 54));
Short = cell2mat(raw(:, 55));


%% Clear temporary variables
clearvars filename delimiter formatSpec fileID dataArray ans raw col numericData rawData row regexstr result numbers invalidThousandsSeparator thousandsRegExp me I J K;

%% Data Analysis

%each row is a trailer, and we have 8 features
master_data = [total_time avg_intensity avg_color_r avg_color_g avg_color_b...
    mean_shot_length std_dev_shot_length max_shot_length min_shot_length...
    num_shots stddev_color_with_letterbox_r stddev_color_with_letterbox_g...
    stddev_color_with_letterbox_b detail_score_mean detail_score_std_dev...
    detail_score_max detail_score_min dark_scene_mean_length...
    dark_scene_length_std_dev dark_scene_length_max	dark_scene_length_min...
    dark_scene_count dark_scene_percentage mean_volume...
    std_dev_volume min_volume max_volume sudden_rise_count_per_cut...
    sudden_fall_count_per_cut];


[num_movies, num_features] = size(master_data); 


%% Testing module
accuracy = [];
num_trials = 40; % number of cross validation trials
accuracy(1) = check_genre_predictions(master_data, Drama, 0.8, num_trials);
accuracy(2) = check_genre_predictions(master_data, Comedy, 0.8, num_trials);
accuracy(3) = check_genre_predictions(master_data, Thriller, 0.8, num_trials);
accuracy(4) = check_genre_predictions(master_data, Action, 0.8, num_trials);
accuracy(5) = check_genre_predictions(master_data, Horror, 0.8, num_trials);
accuracy(6) = check_genre_predictions(master_data, Crime, 0.8, num_trials);
accuracy(7) = check_genre_predictions(master_data, Romance, 0.8, num_trials);
accuracy(8) = check_genre_predictions(master_data, Adventure, 0.8, num_trials);
accuracy(9) = check_genre_predictions(master_data, Biography, 0.8, num_trials);
accuracy(10) = check_genre_predictions(master_data, Documentary, 0.8, num_trials);

%% Plot

success = [];
for j = 1:length(accuracy)
    success(j) = 1 - accuracy(j);
end
    
plot(success, 'ko', 'LineWidth',[2.0]), axis([0 10 .6 1])
   