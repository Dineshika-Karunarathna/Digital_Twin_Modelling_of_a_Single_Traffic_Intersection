
from numpy import array
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import pandas as pd
import matplotlib.pyplot as plt
from google.colab import drive 
drive.mount('/gdrive')
trafficData=pd.read_csv('/gdrive/MyDrive/ML Tutorial/tdata.csv', usecols=[2])
dataset=trafficData.values
dataset=dataset.astype('float32')
from sklearn.preprocessing import MinMaxScaler


scaler = MinMaxScaler(feature_range=(0, 1)) #Also try QuantileTransformer
dataset = scaler.fit_transform(dataset)
def split_sequence(sequence, n_steps):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the sequence
		if end_ix > len(sequence)-1:
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)

train_size = int(len(dataset) * 0.66)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
trainX, trainY = split_sequence(train, n_steps)
print(trainX.size)
testX, testY = split_sequence(test, n_steps)
# define input sequence
#raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90]
# choose a number of time steps

n_steps = 24
seq_size=24
# split into samples
X, y = split_sequence(dataset, n_steps)
# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
#trainX = trainX.reshape((trainX.shape[0], trainX.shape[1], n_features))
#testX = testX.reshape((testX.shape[0], testX.shape[1], n_features))
testY_flat=testY.reshape(-1)
plt.plot(testY_flat)


#Bidirectional LSTM
# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
#
##For some sequence forecasting problems we may need LSTM to learn
## sequence in both forward and backward directions
from keras.layers import Bidirectional
model = Sequential()
model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(None, seq_size)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(trainX, trainY, epochs=5, verbose=1)

model.summary()
print('Train...')
