#lstm model to predict traffic

import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import pandas as pd
import matplotlib.pyplot as plt
import file_handler
import scaler


def  uni_train(learning_rate, batch_size ,epochs,n_steps,n_features,trainX,trainY):

    # define model
    learning_rate = 0.1
    batch_size = 64

    model = Sequential()
    model.add(LSTM(24, activation='relu', input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse',metrics=['MeanSquaredError'])
    # fit model
    #model.fit(X, y, epochs=5, verbose=0,callbacks=[tensorboard_callback])
    hist=model.fit(trainX, trainY ,epochs=2, batch_size=8)
    # demonstrate prediction
    '''x_input = array([15,13,10,7,9,18,9])
    x_input=np.reshape(x_input,(-1,1))
    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0,1))
    x_input=scaler.fit_transform(x_input)
    x_input = x_input.reshape((1, n_steps, n_features))'''

    return model