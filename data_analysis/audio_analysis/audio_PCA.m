%Feature extraction from audio portions of trailers.
clear all; close all; clc;

%Get list of files/ their names
folder_dir = 'C:\Users\Noel_K\git_repository\video-analysis-amath-582\video_processing\clipped';
[mp3_path mp3_dir mp3_file] = dirwalk(folder_dir);
mp3_title{1} = regexprep(mp3_file{1}, '720.\w*$', '');
mp3_title= mp3_title{1};
mp3_file= mp3_file{1};

%How many mp3?
total_n = length(mp3_title);

%Setup time, freq domain for FFT
L=10;
n=44100*10; %Sampling freq of 44100 fps, 10s.
t2=linspace(0,L,n+1); t=t2(1:n);
k=(2*pi/L)*[0:n/2-1 -n/2:-1]; ks=fftshift(k);

magic_number =2227151;
specs = zeros(total_n, magic_number); % the column number determined a posteriori
for j=1: total_n
    %Import audio
    path_file = fullfile(folder_dir, mp3_file(j,1));
    sound = audioread(char(path_file));
    [mp3_length, mp3_channel] = size(sound);
    if mp3_channel ==2
        sound_avg = (sound(:,1) + sound(:,2))/2; %averaging L and R channel
    else
        sound_avg = sound(:,1);
    end
    sound_avg = sound_avg(1:n,1)';
    
    %Windowed FFT
    Sgt_spec=[];
    tslide=0:0.1:L;
        for jj=1:length(tslide)
        g=exp(-20*(t-tslide(jj)).^2); % Gaussian
        Sg=g.*sound_avg; Sgt=fft(Sg);
        Sgt=Sgt(1,n/2:n);
        Sgt_spec=[Sgt_spec; resample(abs(fftshift(Sgt)),1,10)];
%         subplot(3,1,1), plot(t,sound_avg,'k',t,g,'r')
%         subplot(3,1,2), plot(t,Sg,'k')
%         subplot(3,1,3), plot(ks(1,n/2:n),abs(fftshift(Sgt))/max(abs(Sgt)))
%         drawnow
        end
        
    %SVD
    [mm,nn] = size(Sgt_spec);
    Sgt_spec_resized = reshape(Sgt_spec, [1,mm*nn]);
    specs(j,:) =Sgt_spec_resized;
end
%%
%clear temps
clearvars Sg Sgt Sgt_spec Sgt_spec_resized sound sound_avg
avg_spec = mean(specs,2);
specs_avgd = specs-repmat(avg_spec,1, magic_number);
[U, S, V] = svd(specs_avgd/sqrt(magic_number-1),'econ');
Y_prince = U'*specs_avgd; %principal components projection
covar=(1/(magic_number-1))*(Y_prince)*(Y_prince.');
covar_diag = diag(covar);
% t3 = 1:length(covar_diag);
% scatter(t3, covar_diag);
save('audioPCA.mat', 'covar_diag','mp3_title','specs_avgd','Y_prince','U','S','V')
