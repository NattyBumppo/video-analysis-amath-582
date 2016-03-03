%Feature extraction from audio portions of trailers.
clear all; close all; clc;

%Get list of files/ their names
folder_dir = 'C:\Users\Noel\git_repository\video-analysis-amath-582\video_processing\mp3s';
[mp3_path mp3_dir mp3_file] = dirwalk(folder_dir);
mp3_title{1} = regexprep(mp3_file{1}, '.\w*$', '');
mp3_title= mp3_title{1};
mp3_file= mp3_file{1};

%How many mp3?
total_n = length(mp3_title);

%Setup time, freq domain for FFT
sampling_freq=44100; %Sampling freq of 44100 fps, 10s.

band_binned_norm = zeros(total_n, 11);
%audible range of frequency is 20Hz to 20000Hz
%Human ears perceive pitch non-linearly. Use octave band
    %band1(octave1) = 11Hz ~22Hz
    %band2(octave2) = 22Hz ~ 44Hz
    %band3(octave3) = 44Hz ~ 88Hz
    %band4(octave4) = 88Hz ~ 177Hz
    %band5(octave5) = 177Hz ~ 355Hz
    %band6(octave6) = 355Hz ~ 710Hz
    %band7(octave7) = 710Hz ~ 1420Hz
    %band8(octave8) = 1420Hz ~ 2840Hz
    %band9(octave9) = 2840Hz ~ 5680Hz
    %band10(octave10) = 5680Hz ~ 11360Hz
    %band11(octave11) = 11360hz ~ 22720Hz
band_intervals = [11 22 44 88 177 355 710 1420 2840 5680 11360 22720];
ks_indices_for_cut = zeros(1,11);
for j=1: total_n
    %Import audio
    path_file = fullfile(folder_dir, mp3_file(j,1));
    sound = audioread(char(path_file));
    [mp3_length mp3_channel] = size(sound);
    
    n= mp3_length;
    L= mp3_length/sampling_freq;    %audio length in second
    t2=linspace(0,L,n+1); t=t2(1:n);
    k=(2*pi/L)*[0:n/2-1 -n/2:-1]; ks=fftshift(k);
    
    %averaging L and R channel for brevity. No need if its already mono
    if mp3_channel == 2
        sound_avg = (sound(:,1) + sound(:,2))/2; 
        sound_avg = sound_avg(1:n,1)';
    else
        sound_avg = sound(1:n,1)';
    end
    
    %fft
    sound_avg_t = fft(sound_avg);
    sound_avg_t_s= fftshift(sound_avg_t);
    sound_avg_t_s_abs = abs(sound_avg_t_s);
    
    band_sum = zeros(11,1); %pre-populate
    for jj=1:12
    %find indices in ks corresponding to frequency bands (freq in Hz =
    %ks(waveno. /2*pi
    [idx idx] = min(abs(ks/(2*pi)-band_intervals(jj)));
    ks_indices_for_cut(jj) = idx;
    end
    for jj=1:11
    band_sum(jj,1) = sum(sound_avg_t_s_abs(1,ks_indices_for_cut(jj):ks_indices_for_cut(jj+1)));
    end
    band_total_sum = sum(band_sum);
    band_sum_norm = band_sum./band_total_sum;
    band_binned_norm(j,:) = band_sum_norm';
end
save('audio_freq_bin.mat', 'band_binned_norm','mp3_title','mp3_file','total_n')
