from numpy import array
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import pandas as pd
import matplotlib.pyplot as plt
import file_handler
import scale
import split_data
import lstm_mod
import model_eval



traffic_data = pd.read_csv('D:\\Acedamic\\FYP\\Codes\\Datasets\\3_way.csv')
traffic_data.dropna(inplace=True)
dataset=traffic_data.values

print(dataset)


##############################################################################################
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

dataset= scale.scale_data(dataset,scaler)
print(dataset)

N_S=traffic_data['N_S']
N_W=traffic_data['N_W']
S_N=traffic_data['S_N']
S_W=traffic_data['S_W']
W_N=traffic_data['W_N']
W_S=traffic_data['W_S']

plt.plot(N_S)
plt.show()





n_steps=24

train_size = int(len(dataset) * 0.66)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
trainX, trainY = split_data.split_sequence(train, n_steps)
testX, testY = split_data.split_sequence(test, n_steps)

print(trainX.shape, trainY.shape)
print(testX.shape, testY.shape)


# define input sequence
#raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90]
# choose a number of time steps
n_steps = 24
# split into samples
X, y = split_data.split_sequence(dataset, n_steps)
# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
trainX = trainX.reshape((trainX.shape[0], trainX.shape[1], n_features))
testX = testX.reshape((testX.shape[0], testX.shape[1], n_features))
print(trainX.shape, trainY.shape)
print(testX.shape, testY.shape)

testY_flat=testY.reshape(-1)
plt.plot(testY_flat)
plt.show()



