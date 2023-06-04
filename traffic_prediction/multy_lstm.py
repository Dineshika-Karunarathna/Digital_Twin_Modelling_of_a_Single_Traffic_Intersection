from numpy import array
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import pandas as pd
import matplotlib.pyplot as plt
import file_handler
import scaler
import split_data
import lstm_mod



dataset=file_handler.get_data('cleanedkaggleTrafic.csv')

print(dataset)
plt.plot(dataset)
plt.show()
print(len(dataset))

dataset= scaler.scale_data(dataset)
print(dataset)

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



# define model
learning_rate = 0.1
batch_size = 64
epochs=2



lstm_mod.uni_train(learning_rate, batch_size ,epochs,n_steps,n_features,trainX,trainY)

