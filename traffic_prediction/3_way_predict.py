import pickle 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import file_handler
import scale

folder_path = 'D:\Acedamic\FYP\Codes\DTMSTI\Digital_Twin_Modelling_of_a_Single_Traffic_Intersection\\traffic_prediction\Models\weights'

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
    filename = f'model_{i}.pkl'
    file_path = os.path.join(folder_path, filename)
    



    with open(file_path, 'rb') as file:
        loaded_model = pickle.load(file)

    # Perform inference or further operations with the loaded model
    #predictions = loaded_model.predict(X_test)


