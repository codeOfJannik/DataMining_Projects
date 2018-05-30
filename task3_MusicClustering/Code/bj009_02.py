import pandas as pd
import numpy as np
import os.path
import scipy
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing


# Function to read CSV-files into pandas dataFrames
def fromCSVtoDataframe():

    train = pd.read_csv('FeatureFileTrainingAllList1.csv')
    test = pd.read_csv('FeatureFileTestAllList2.csv')

    X = preprocessing.scale(train)







fromCSVtoDataframe()