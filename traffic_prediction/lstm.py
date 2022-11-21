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