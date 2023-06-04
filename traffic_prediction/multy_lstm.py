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



dataset=file_handler.get_data('cleanedkaggleTrafic.csv')

print(dataset)
plt.plot(dataset)
plt.show()
print(len(dataset))

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

dataset= scale.scale_data(dataset,scaler)
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
epochs=20



model=lstm_mod.uni_train(learning_rate, batch_size ,epochs,n_steps,n_features,trainX,trainY)

train_predict = model.predict(trainX, verbose=0)
test_predict = model.predict(testX, verbose=0)

print(train_predict)


Scaled_trainPredict = scaler.inverse_transform(train_predict)
Scaled_trainY = scaler.inverse_transform(trainY)
Scaled_testPredict = scaler.inverse_transform(test_predict)
Scaled_testY = scaler.inverse_transform(testY)

trainY_flat=Scaled_trainY.reshape(-1)
plt.plot(trainY_flat)

trainPredict_flat=Scaled_trainPredict.reshape(-1)
plt.plot(trainPredict_flat)
plt.legend('Ground Turth','Prediction')
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(Scaled_trainY[:48], label="Ground Turth")
plt.plot(trainPredict_flat[:48],label="Prediction")
plt.legend(loc="upper left")

plt.show()

testY_flat=Scaled_testY.reshape(-1)
plt.plot(testY_flat)
testPredict_flat=Scaled_testPredict.reshape(-1)
plt.plot(testPredict_flat)
plt.legend('Ground Turth','Prediction')
plt.legend(loc="upper left")

plt.show()

plt.figure(figsize=(10, 5))

plt.plot(Scaled_testY[:48],label="Ground Turth")
plt.plot(testPredict_flat[:48],label="Prediction")
#plt.xlabel('Hours')
plt.ylabel('Traffic')
plt.legend(loc="upper left")

plt.show()

print(model.summary())

print('Train')
model_eval.mae(Scaled_trainY,trainPredict_flat)
model_eval.mse(Scaled_trainY,trainPredict_flat)
model_eval.rmse(Scaled_trainY,trainPredict_flat)
print('Test')
model_eval.mae(Scaled_testY,testPredict_flat)
model_eval.mse(Scaled_testY,testPredict_flat)
model_eval.rmse(Scaled_testY,testPredict_flat)


