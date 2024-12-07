# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zsvPlSNe9Squ3aKUC9C3YdrmRYNbds3Q
"""

#import libraries (some of them may not be used)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
import random
import keras
from keras.layers import GlobalAveragePooling2D, GlobalMaxPooling2D, Reshape, Dense, multiply, Permute, Concatenate, Conv2D, Add, Activation, Lambda
from keras import backend as K
from keras.activations import sigmoid
from keras import layers
from keras import initializers
from keras.models import Sequential
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Flatten, Dropout, BatchNormalization,Embedding, LSTM, Reshape, Bidirectional,Conv1D, MaxPooling1D, AveragePooling1D, Conv2D, MaxPooling2D, Conv3D, MaxPooling3D
from tensorflow.keras.callbacks import ModelCheckpoint
import wave
import os.path
from pathlib import Path
from keras import regularizers
from keras.preprocessing import sequence
from keras.utils import pad_sequences
from keras.models import Sequential, Model, model_from_json, load_model
from keras.layers import Input, Flatten, Dropout, Activation, BatchNormalization
from keras.callbacks import (EarlyStopping, LearningRateScheduler,
                             ModelCheckpoint, TensorBoard, ReduceLROnPlateau)
from keras import losses, models, optimizers
from keras.activations import relu, softmax
from tensorflow.keras.utils import to_categorical, custom_object_scope
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm, tqdm_pandas
import scipy
import librosa
import librosa.display
import json
from matplotlib.pyplot import specgram
import seaborn as sns
import glob
import sys
import warnings
# ignore warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

#Connecting to our google drive to access our data
from google.colab import drive
drive.mount('/content/drive')

"""Feature Extraction (20 MFCC features from Vowel /i/ in AVFAD dataset)"""

b1=[]
b2=[]
b3=[]

#extracting MFCC features from the train data and put them in a list whit their filenames

for file in glob.glob("/content/drive/MyDrive/train_01/train1/*.wav"):

        y1, sr1 = librosa.load(file, sr = None, mono=True)
        mfccs1= librosa.feature.mfcc(y=y1, sr=sr1, n_mfcc=20)
        filename1 = Path(file).stem
        x1 = filename1.split("_")
        b1.append([x1[0],mfccs1])

#extracting MFCC features from the validation data and put them in a list whit their filenames

for file in glob.glob("/content/drive/MyDrive/valid_01/validation1/*.wav"):

        y2, sr2 = librosa.load(file, sr = None, mono=True)
        mfccs2= librosa.feature.mfcc(y=y2, sr=sr2,n_mfcc=20)
        filename2 = Path(file).stem
        x2 = filename2.split("_")
        b2.append([x2[0],mfccs2])

#extracting MFCC features from the test data and put them in a list whit their filenames

for file in glob.glob("/content/drive/MyDrive/test_01/test1/*.wav"):

        y3, sr3 = librosa.load(file, sr = None, mono=True)
        mfccs3= librosa.feature.mfcc(y=y3, sr=sr3, n_mfcc=20)
        filename3 = Path(file).stem
        x3 = filename3.split("_")
        b3.append([x3[0],mfccs3])

"""Because the number of frames for each sample is differen, here we get the (Average + STD) of the frame numbers for the Dataset(train + valid + test)."""

f1 = []
f2 = []
f3 = []

for i in range (460):
  f1.append(len((b1[i][1]).T))
for i in range (105):
  f2.append(len((b2[i][1]).T))
for i in range (142):
  f3.append(len((b3[i][1]).T))

f4 = f1 + f2 + f3

F4 = np.array(f4)

ave = np.mean(F4)
s = np.std(F4)
print(min(F4))
print(ave)
print(s)
print(ave+s)

"""Making X_train, X_test, X_validation and Y_train, Y_test, Y_validation"""

d1=[]
d2=[]
d3=[]

for i in range(460):
        d1.append([b1[i][0], ((b1[i][1]).T)[0:2095]])
for i in range(105):
        d2.append([b2[i][0], ((b2[i][1]).T)[0:2095]])
for i in range(142):
        d3.append([b3[i][0], ((b3[i][1]).T)[0:2095]])

data_train_MFCC =[]
data_valid_MFCC =[]
data_test_MFCC =[]

#we get our labels for each sample from this file

df = pd.read_csv('/content/drive/MyDrive/AVFAD_01_00_00.csv', encoding='ISO-8859-1')

for i in range(460):
    for j in range(709):
        if d1[i][0] == df.iloc[j,0]:
            data_train_MFCC.append([d1[i][0], d1[i][1], df.iloc[j,15]])

for i in range(105):
    for j in range(709):
        if d2[i][0] == df.iloc[j,0]:
            data_valid_MFCC.append([d2[i][0], d2[i][1], df.iloc[j,15]])

for i in range(142):
    for j in range(709):
        if d3[i][0] == df.iloc[j,0]:
            data_test_MFCC.append([d3[i][0], d3[i][1], df.iloc[j,15]])

data_train_MFCC.sort(key = lambda x: x[0])
data_valid_MFCC.sort(key = lambda x: x[0])
data_test_MFCC.sort(key = lambda x: x[0])

y_train = []
y_valid = []
y_test = []

x_train_MFCC = []
x_valid_MFCC = []
x_test_MFCC = []

for i in range(460):
    x_train_MFCC.append(data_train_MFCC[i][1])
for i in range(105):
    x_valid_MFCC.append(data_valid_MFCC[i][1])
for i in range(142):
    x_test_MFCC.append(data_test_MFCC[i][1])

for i in range(460):
    y_train.append(data_train_MFCC[i][2])
for i in range(105):
    y_valid.append(data_valid_MFCC[i][2])
for i in range(142):
    y_test.append(data_test_MFCC[i][2])

y_train = [0 if label == 'Normal' else 1 for label in y_train]
y_test = [0 if label == 'Normal' else 1 for label in y_test]
y_valid = [0 if label == 'Normal' else 1 for label in y_valid]

Y_train = np.array(y_train)
Y_valid = np.array(y_valid)
Y_test = np.array(y_test)

"""For having same frame numbers, here we add zero instead of features for samples that they have less frames than the 'Average + STD' of all samples' frame numbers."""

z = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Z = np.array(z)
for i in range (20):
  Z[i]=np.float64(Z[i])

for i in range(460):
  for j in range(2095-len(x_train_MFCC[i])):
     x_train_MFCC[i] = np.append(x_train_MFCC[i], [Z], axis=0)
for i in range(105):
  for j in range(2095-len(x_valid_MFCC[i])):
     x_valid_MFCC[i] = np.append(x_valid_MFCC[i], [Z], axis=0)
for i in range(142):
  for j in range(2095-len(x_test_MFCC[i])):
     x_test_MFCC[i] = np.append(x_test_MFCC[i], [Z], axis=0)

X_train_MFCC = np.array(x_train_MFCC)
X_valid_MFCC = np.array(x_valid_MFCC)
X_test_MFCC = np.array(x_test_MFCC)

"""Normalization"""

import numpy as np

def z_score_normalize(data, mean=None, std=None):
    if mean is None:
        mean = np.mean(data, axis=(0, 1))
    if std is None:
        std = np.std(data, axis=(0, 1))
    normalized_data = (data - mean) / std
    return normalized_data, mean, std

# Calculate mean and std from train_data and normalize all datasets

X_train_MFCC, mean2, std2 = z_score_normalize(X_train_MFCC)
X_test_MFCC, _, _ = z_score_normalize(X_test_MFCC, mean2, std2)
X_valid_MFCC, _, _ = z_score_normalize(X_valid_MFCC, mean2, std2)

"""The Proposed Optomal CNN Model for Training our Dataset"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dropout, Dense

model_CNN_small = Sequential()
# Convolutional Layers
model_CNN_small.add(Conv2D(8, (3, 3), input_shape=(2095, 20, 1), activation='relu', padding='same'))
model_CNN_small.add(MaxPooling2D(pool_size=(2, 2)))

model_CNN_small.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
model_CNN_small.add(MaxPooling2D(pool_size=(2, 2)))

model_CNN_small.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model_CNN_small.add(MaxPooling2D(pool_size=(2, 2)))

# Global Average Pooling
model_CNN_small.add(GlobalAveragePooling2D())

# Regularization
model_CNN_small.add(Dropout(0.3))

# Fully Connected Layers
model_CNN_small.add(Dense(64, activation='relu'))
model_CNN_small.add(Dropout(0.2))

model_CNN_small.add(Dense(1, activation='sigmoid'))

# Compile the model
model_CNN_small.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print the model summary
model_CNN_small.summary()

#saving the trained model
filepath_MFCC = '/content/sample_data/model_test_MFCC.keras'
checkpoint = ModelCheckpoint(filepath=filepath_MFCC,
                             monitor='val_accuracy',
                             verbose=0,
                             save_best_only=True,
                             mode='max')
callbacks = [checkpoint]

import time
import subprocess


# Record the start time
start_time = time.time()

# Train the model
history = model_CNN_small.fit(X_train_MFCC, Y_train,
                        validation_data=(X_valid_MFCC, Y_valid),
                        batch_size=64, epochs=200,
                        callbacks=callbacks)

# Calculate total training time
total_time = time.time() - start_time


# Print the results
print(f"Total training time: {total_time:.2f} seconds")

"""Accuracies of the model for test and validation data by MFCC Features for vowel /i/"""

from keras.models import load_model

model = load_model(filepath_MFCC)

test_loss, test_acc = model.evaluate(X_valid_MFCC,Y_valid, verbose=0)
print("validation Accuracy by MFCC: ",test_acc)

test_loss, test_acc = model.evaluate(X_test_MFCC,Y_test, verbose=0)
print("Test Accuracy by MFCC: ",test_acc)

"""Training Accuracy Plot"""

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Training', 'Validation'])
plt.show()

y_pred=model.predict(X_test_MFCC)

"""Reporting Precision, Recall, and F1-Score for Healthy and Unhealthy Samples"""

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(Y_test, y_pred.round()))
print(classification_report(Y_test, y_pred.round()))