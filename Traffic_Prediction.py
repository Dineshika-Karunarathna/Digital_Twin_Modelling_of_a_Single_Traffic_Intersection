import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt  
import tensorflow as tf  
from tensorflow import keras
import seaborn as sn 

#trafficData=pd.read_csv('D:\\Acedamic\\FYP\\Codes\\Datasets\\tdata.csv',parse_dates=['DateTime',index_col='DateTime'])
trafficData=pd.read_csv('D:\\Acedamic\\FYP\\Codes\\Datasets\\tdata.csv',parse_dates=['DateTime'])
print(trafficData.head(10))
print(len(trafficData))
print(list(trafficData.columns))

x=trafficData['DateTime']
y=trafficData['Vehicles']
#plt.plot(x,y)
#plt.show()
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
print(len(x_train))

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x_train) 
train_scaled = scaler.transform(x_train)
test_scaled = scaler.transform(x_test)

