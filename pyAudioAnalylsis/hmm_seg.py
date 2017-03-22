# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:04:59 2017

@author: spnichol
"""
import csv
import pandas as pd
from numpy import nan
import subprocess
from subprocess import call 
import re
import soundfile as sf
from os import listdir
from os.path import isfile, join
import wave

def dl_vids():
    vidlist = pd.read_csv('vidlist.csv', parse_dates=True)
    for index, row in vidlist.iterrows():
    
        vidname = row["VidName"]+".mp4"
        link = row["YouLink"]
        vidname= row["Folder"]+"/"+vidname
        print link
    #
        print subprocess.call(['youtube-dl',link,  "--output", vidname, "--extract-audio","--audio-format", "wav"])
        aud_name2 = row["Folder"]+"/"+row["VidName"]+".wav"
    
    
def test_vids():
    testlist = pd.read_csv('testlist.csv', parse_dates=True)
    for index, row in testlist.iterrows():
    
        vidname = row["VidName"]+".mp4"
        link = row["YouLink"]
        vidname= row["Folder"]+"/"+vidname
        print link
    #
        print subprocess.call(['youtube-dl',link,  "--output", vidname, "--extract-audio","--audio-format", "wav"])
        aud_name2 = row["Folder"]+"/"+row["VidName"]+".wav"

def music():
    vidlist = pd.read_csv('vidlist.csv', parse_dates=True)
    for index, row in vidlist.iterrows():
        if "music" in row["VidName"]:
        
            vidname = row["VidName"]+".mp4"
            link = row["YouLink"]
            vidname= row["Folder"]+"/"+vidname
            print link
        #
            print subprocess.call(['youtube-dl',link,  "--output", vidname, "--extract-audio","--audio-format", "wav"])
            aud_name2 = row["Folder"]+"/"+row["VidName"]+".wav"
        else: 
            print "nothing to do" 
def one_off(link, vidname, folder):   
    link = link 
    vidname = folder+vidname+".mp4"
    print subprocess.call(['youtube-dl',link,  "--output", vidname, "--extract-audio","--audio-format", "wav"])


#convert sampling rate 
def samp_rate(wav_dir):
    
    wav_files = [f for f in listdir(wav_dir) if isfile(join(wav_dir, f))]
    for wav_file in wav_files:
        f = sf.SoundFile(wav_dir+"/"+ wav_file)
        file_name = ('samples = {}'.format(len(f)))
        sample_rate = ('sample rate = {}'.format(f.samplerate))
        print(sample_rate)
        if f.samplerate != 44100:
            new_wav = wave.open(wav_dir+"/"+ wav_file, "rb")
            width = new_wav.getsampwidth()  
            nchannels = new_wav.getnchannels()
            nframes = len(f)
            new_wav2 = wave.open(wav_dir + "/" + wav_file, "wb")

            new_wav2.setframerate(44100)
            new_wav2.setparams((nchannels, width, 44100, nframes, 'NONE', 'Uncompressed'))
            new_wav2.close()
def samp_rate_small(wav_dir):
    
    wav_files = [f for f in listdir(wav_dir) if isfile(join(wav_dir, f))]
    for wav_file in wav_files:
        f = sf.SoundFile(wav_dir+"/"+ wav_file)
        file_name = ('samples = {}'.format(len(f)))
        sample_rate = ('sample rate = {}'.format(f.samplerate))
        print(sample_rate)
        if f.samplerate != 16000:
            new_wav = wave.open(wav_dir+"/"+ wav_file, "rb")
            width = new_wav.getsampwidth()  
            nchannels = new_wav.getnchannels()
            nframes = len(f)
            new_wav2 = wave.open(wav_dir + "/" + wav_file, "wb")

            new_wav2.setframerate(16000)
            new_wav2.setparams((nchannels, width, 16000, nframes, 'NONE', 'Uncompressed'))
            new_wav2.close()
            

def amlo_split():
    amlo_files = [f for f in listdir("amlo") if isfile(join("amlo", f))]
    for file in amlo_files:
        file = "amlo/"+file
        command = "ffmpeg -i "+file+ " -c copy -map 0 -segment_time 10 -f segment " +file+"output%03d.wav"
        subprocess.call(command, shell=True)

def not_amlo_split():
    not_amlo_files = [f for f in listdir("not_amlo") if isfile(join("not_amlo", f))]
    for file in not_amlo_files:
        file = "not_amlo/"+file
        command = "ffmpeg -i "+file+ " -c copy -map 0 -segment_time 10 -f segment " +file+"output%03d.wav"
        subprocess.call(command, shell=True)

def music_split():
    music_files = [f for f in listdir("music") if isfile(join("music", f))]
    for file in music_files:
        file = "music/"+file
        command = "ffmpeg -i "+file+ " -c copy -map 0 -segment_time 10 -f segment " +file+"output%03d.wav"
        subprocess.call(command, shell=True)


def check_size():
    not_amlo_files = [f for f in listdir("not_amlo") if isfile(join("not_amlo", f))]
    for wav_file in not_amlo_files:
        f = sf.SoundFile("not_amlo/"+ wav_file)
        file_name = ('samples = {}'.format(len(f)))
        sample_rate = ('sample rate = {}'.format(f.samplerate))

        sample_length = len(f) / f.samplerate
        print len(f)
        if sample_length != 10:
            import os
            print "removing" + wav_file 
            os.remove("not_amlo/"+wav_file)
    amlo_files = [f for f in listdir("amlo") if isfile(join("amlo", f))]
    for wav_file in amlo_files:
        f = sf.SoundFile("amlo/"+ wav_file)
        file_name = ('samples = {}'.format(len(f)))
        sample_rate = ('sample rate = {}'.format(f.samplerate))

        sample_length = len(f) / f.samplerate
        print len(f)
        if sample_length != 10:
            import os
            print "removing" + wav_file 
            os.remove("amlo/"+wav_file)
    music_files = [f for f in listdir("music") if isfile(join("music", f))]
    for wav_file in music_files:
        f = sf.SoundFile("music/"+ wav_file)
        file_name = ('samples = {}'.format(len(f)))
        sample_rate = ('sample rate = {}'.format(f.samplerate))
        sample_length = len(f) / f.samplerate
        print len(f)

        if sample_length != 10:
            print "removing" + wav_file 
            os.remove("music/"+wav_file)
            
#one_off("www.youtube.com/watch?v=RoTKbD2SNI8", "amlo6.wav", "amlo/")            
test_vids()           
#samp_rate("amlo")
#samp_rate("not_amlo")
#
#samp_rate("test")

#amlo_split()
#not_amlo_split()
#music_split()
#check_size()
#python audioAnalysis.py classifyFile -i amlo4.wav --model svm --classifier data/svmMusicGenre3
  
#python audioAnalysis.py trainClassifier -i data/amlo data/not_amlo --method knn -o data/amloKNN
#python audioAnalysis.py trainClassifier -i data/amlo data/not_amlo --method svm -o data/amlo2SVM
#python audioAnalysis.py segmentClassifyFile -i test/amlo.wav --model knn --modelName data/amloKNN
#python audioAnalysis.py segmentClassifyFile -i test/amlo_mix.wav --model svm --modelName data/amlo2SVM
#python audioAnalysis.py speakerDiarization -i test/amlo_mix.wav --num 0 
#python audioAnalysis.py trainHMMsegmenter -i data/amlo -o data/not_amlo -mw 1.0 -ms 1.0  
#trainHMMsegmenter_fromfile
#python audioAnalysis.py trainHMMsegmenter_fromfile -i data/amlo -o data/not_amlo -mw 1.0 -ms 1.0  

#python audioAnalysis.py classifyFolder -i test/ --model svm --classifier data/amlo2SVM
#python audioAnalysis.py classifyFolder -i data/recording3_ --model svm --classifier data/svmSM --detail


#python audioAnalysis.py segmentClassifyFile -i test/amlo.wav --model svm --modelName data/amlo2SVM