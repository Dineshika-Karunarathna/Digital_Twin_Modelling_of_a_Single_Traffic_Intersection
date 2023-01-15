import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from sklearn import linear_model
from sklearn import *


trafficData=pd.read_csv('D:\\Acedamic\\FYP\\Codes\\Datasets\\tdata.csv', usecols=[2])
dataset=trafficData.values
dataset=dataset.astype('float32')
from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
dataset=scaler.fit_transform(dataset)
#train_size=int(len(dataset)*0.66)
train_size=int(len(dataset)*0.7)
test_size=len(dataset)-train_size
train,test=dataset[0:train_size,:],dataset[train_size:len(dataset),:] 
print (len(train),len(test))   

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
	return np.array(X), np.array(y)

def neurons():
	neurons = []
	for i in range(1, 100):
		neurons.append(i)
	#return neurons
	# define model
	learning_rate = 0.1
	batch_size = 64

