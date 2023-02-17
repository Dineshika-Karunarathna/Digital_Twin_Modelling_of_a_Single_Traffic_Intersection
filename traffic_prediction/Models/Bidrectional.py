
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