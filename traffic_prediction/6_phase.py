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
N_S=traffic_data['N_S']
N_W=traffic_data['N_W']
S_N=traffic_data['S_N']
S_W=traffic_data['S_W']
W_N=traffic_data['W_N']
W_S=traffic_data['W_S']

print(N_W)