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

train_size=int(len(dataset)*0.66)
test_size=len(dataset)-train_size
train,test=dataset[0:train_size,:],dataset[train_size:len(dataset),:] 
print (len(train),len(test))   

import random
import matplotlib.pyplot as pltgit 
