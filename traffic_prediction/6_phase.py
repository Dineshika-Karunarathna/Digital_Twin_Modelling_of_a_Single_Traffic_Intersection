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



traffic_data = pd.read_csv('3_way.csv',usecols=[2])
traffic_data.dropna(inplace=True)
dataset=traffic_data.values

print(dataset)