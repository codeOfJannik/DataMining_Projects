import subprocess
import wave
import struct
import numpy
import os
import pandas as pd

numpy.set_printoptions(precision=2, suppress=True)

# Names of features extracted in this module
FeatNames = ["amp1mean", "amp1std", "amp1skew", "amp1kurt", "amp1dmean", "amp1dstd", "amp1dskew", "amp1dkurt",
             "amp10mean", "amp10std",
             "amp10skew", "amp10kurt", "amp10dmean", "amp10dstd", "amp10dskew", "amp10dkurt", "amp100mean", "amp100std",
             "amp100skew",
             "amp100kurt", "amp100dmean", "amp100dstd", "amp100dskew", "amp100dkurt", "amp1000mean", "amp1000std",
             "amp1000skew",
             "amp1000kurt", "amp1000dmean", "amp1000dstd", "amp1000dskew", "amp1000dkurt", "power1", "power2", "power3",
             "power4",
             "power5", "power6", "power7", "power8", "power9", "power10"]


def moments(x):
    mean = x.mean()
    std = x.var() ** 0.5
    skewness = ((x - mean) ** 3).mean() / std ** 3
    kurtosis = ((x - mean) ** 4).mean() / std ** 4
    return [mean, std, skewness, kurtosis]


# Feature category 2: Frequency domain parameters
def fftfeatures(wavdata):
    f = numpy.fft.fft(wavdata)
    f = f[2:(int(f.size / 2) + 1)]
    f = abs(f)
    total_power = f.sum()
    f = numpy.array_split(f, 10)
    return [e.sum() / total_power for e in f]


# Creating the entire feature vector per music-file
def features(x):
    x = numpy.array(x)
    f = []

    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 10).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 100).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 1000).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    f.extend(fftfeatures(x))
    return f


def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""
    w = wave.open(wav_file)
    n = 60 * 10000
    if w.getnframes() < n * 3:
        raise ValueError('Wave file too short')
    # For each music file 2 sequences, each containing n frames are subtracted. The first sequence starts at postion n,
    # the second sequence starts at postion 2n. The reason for extracting 2 subsequences is, that later on we like to
    # find the best features and in this exercise we assume that good features have the property that they are similar for 2 subsequences
    # of the same song, but differ for subsequences of different songs.
    w.setpos(n)
    frames = w.readframes(n)
    wav_data1 = struct.unpack('%dh' % n, frames)
    frames = w.readframes(n)
    wav_data2 = struct.unpack('%dh' % n, frames)
    return wav_data1, wav_data2


def compute_chunk_features(mp3_file):
    """Return feature vectors for two chunks of an MP3 file."""
    # Extract MP3 file to a mono, 10kHz WAV file
    # mpg123_command = 'C:\Program Files (x86)\mpg123-1.22.0-x86\mpg123-1.22.0-x86\\mpg123.exe -w "%s" -r 10000 -m "%s"'
    # mpg123_command = 'C:\\Program Files (x86)\\mpg123-1.21.0-x86-64\\mpg123.exe -w "%s" -r 10000 -m "%s"'
    # mpg123_command = 'C:\Users\maucher\Downloads\mpg123-1.23.8-x86-64\mpg123-1.23.8-x86-64\\mpg123.exe -w "%s" -r 10000 -m "%s"'
    mpg123_command = '/usr/local/Cellar/mpg123/1.25.10/bin/mpg123 -w "%s" -r 10000 -m "%s"'
    out_file = 'temp.wav'
    cmd = mpg123_command % (out_file, mp3_file)
    temp = subprocess.call(cmd, shell=True)
    # Read in chunks of data from WAV file
    wav_data1, wav_data2 = read_wav(out_file)
    # We'll cover how the features are computed in the next section!
    return numpy.array(features(wav_data1)), numpy.array(features(wav_data2))


fileList = []
featureList1 = []
featureList2 = []
# Specify the name of the directory, which contains your MP3 files here.
# This directory should contain for each band/author one subdirectory, which contains all songs of this author
for path, dirs, files in os.walk('./../../Resources/BandCollection'):
    # print '-'*10,dirs,files
    for f in files:
        if not f.endswith('.mp3'):
            # Skip any non-MP3 files
            continue
        mp3_file = os.path.join(path, f)
        print (mp3_file)
        # Extract the track name (i.e. the file name) plus the names
        # of the two preceding directories. This will be useful
        # later for plotting.
        tail, track = os.path.split(mp3_file)
        tail, dir1 = os.path.split(tail)
        tail, dir2 = os.path.split(tail)
        # Compute features. feature_vec1 and feature_vec2 are lists of floating
        # point numbers representing the statistical features we have extracted
        # from the raw sound data.
        try:
            feature_vec1, feature_vec2 = compute_chunk_features(mp3_file)
        except:
            print ("Error: Chunk Features failed")
            continue
        # title=str(track)
        title = str(dir1) + '\\' + str(track)
        print ('-' * 20 + title + '-' * 20)
        # print "       feature vector 1:",feature_vec1
        # print "       feature vector 2:",feature_vec2
        fileList.append(title)
        featureList1.append(feature_vec1)
        featureList2.append(feature_vec2)

# Write feature vecotrs of all music files to pandas data-frame
MusicFeaturesTrain = pd.DataFrame(index=fileList, data=numpy.array(featureList1), columns=FeatNames)
MusicFeaturesTrain.to_csv("FeatureFileTrainingAllList1.csv")

MusicFeaturesTest = pd.DataFrame(index=fileList, data=numpy.array(featureList2), columns=FeatNames)
MusicFeaturesTest.to_csv("FeatureFileTestAllList2.csv")
