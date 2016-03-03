clc; close all;
%%
%Import CSV
load C:\Users\Noel\git_repository\GitTest\Noel\audio_freq_bin.mat
% Initialize variables.
filename = 'C:\Users\Noel\git_repository\video-analysis-amath-582\video_processing\more_trailer_dataNOCOMMA.csv';
delimiter = ',';

% Read columns of data as strings:
% For more information, see the TEXTSCAN documentation.
formatSpec = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%*s%*s%*s%*s%*s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%[^\n\r]';

% Open the text file.
fileID = fopen(filename,'r');

% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray_orig = textscan(fileID, formatSpec, 'Delimiter', delimiter,  'ReturnOnError', false);
titleArray = dataArray_orig{1};
dataArray= dataArray_orig(2:end);

% Close the text file.
fclose(fileID);
%%
%mp3 order and trailer list orders are different. Get proper indices
mp3_in_trailer_idx = zeros(total_n,1);
cellfind = @(string)(@(cell_contents)(strcmp(string,cell_contents)));
for j=1:total_n
    mp3_in_trailer_idx(j) = find(cellfun(cellfind(char(mp3_title(j))),titleArray));
end
%%
%append to CSV
headers = {'octave1', 'octave2', 'octave3', 'octave4', 'octave5', 'octave6','octave7', 'octave8', 'octave9', 'octave10', 'octave11'};
%%
[null, no_features] = size(dataArray_orig);
[no_trailers, null ] = size(dataArray_orig{1});
dataArray_new = cell(no_trailers, no_features+11);

for j= 1: no_features
    if (1<=j) && (j<=31)
        dataArray_new(:,j) = dataArray_orig{j}(:); %these columns remain unchanged
    elseif (32<=j) && (j<=42)
        %setup headers
        str= cellstr(headers{j-31});
        dataArray_new(1,j) = str;
        for jj=1:total_n
            dataArray_new(mp3_in_trailer_idx(jj),j)=num2cell(band_binned_norm(jj,j-31));
        end                     
        dataArray_new(:,j+11) = dataArray_orig{j}(:);
    else
        dataArray_new(:,j+11) = dataArray_orig{j}(:); %these columns remain unchanged
    end
end

%%
%export
cell2csv('more_trailer_dataNOCOMMA_w_octave.csv', dataArray_new, ',' ,2000,[])
