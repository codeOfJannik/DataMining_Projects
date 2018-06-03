import pandas as pd
import numpy as np
import os.path
import scipy
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing


#Names of features extracted in this module
FeatNames=["amp1mean","amp1std","amp1skew","amp1kurt","amp1dmean","amp1dstd","amp1dskew","amp1dkurt","amp10mean","amp10std",
           "amp10skew","amp10kurt","amp10dmean","amp10dstd","amp10dskew","amp10dkurt","amp100mean","amp100std","amp100skew",
           "amp100kurt","amp100dmean","amp100dstd","amp100dskew","amp100dkurt","amp1000mean","amp1000std","amp1000skew",
           "amp1000kurt","amp1000dmean","amp1000dstd","amp1000dskew","amp1000dkurt","power1","power2","power3","power4",
           "power5","power6","power7","power8","power9","power10"]



# Function to read CSV-files into pandas dataFrames
def fromCSVtoDataframe():

    df_train = pd.read_csv('FeatureFileTrainingAllList1.csv')
    df_test = pd.read_csv('FeatureFileTestAllList2.csv')

    train = df_train.drop('Unnamed: 0',axis=1)
    test = df_test.drop('Unnamed: 0',axis=1)


    train_scaled = preprocessing.scale(train,axis=0,with_mean=True,with_std=True)
    test_scaled = preprocessing.scale(test,axis=0,with_mean=True,with_std=True)

    print train_scaled
    print test_scaled

fromCSVtoDataframe()