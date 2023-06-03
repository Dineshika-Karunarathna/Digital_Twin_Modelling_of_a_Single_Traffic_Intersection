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