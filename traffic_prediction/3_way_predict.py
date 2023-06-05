import pickle 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
import file_handler
import scale
import split_data
import lstm_mod
import model_eval

traffic_data = pd.read_csv('D:\\Acedamic\\FYP\\Codes\\Datasets\\3_way.csv')
traffic_data.dropna(inplace=True)
traffic_data = traffic_data.drop(columns=['Frame', '5 Minute'])

data=[]
for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
    data.append(traffic_data[phase].values)

Scalers=[]
for i in range(6):
    Scalers.append(MinMaxScaler(feature_range=(0, 1)))

for i in range(6):
    data[i]=Scalers[i].fit_transform(data[i].reshape(-1,1))

n_steps=39
n_features = 1

def split(n_steps,dataset):
    testX, testY = split_data.split_sequence(dataset, n_steps)
    testX = testX.reshape((testX.shape[0], testX.shape[1], n_features))
    testY_flat=testY.reshape(-1)
    plt.plot(testY_flat)
    plt.show()
    return testX,testY


testX=[]
testY=[]
Test_Predict=[]
predictions={}









folder_path = 'D:\Acedamic\FYP\Codes\DTMSTI\Digital_Twin_Modelling_of_a_Single_Traffic_Intersection\\traffic_prediction\Models\weights'

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
    filename = f'model_{i}.pkl'
    file_path = os.path.join(folder_path, filename)
    



    with open(file_path, 'rb') as file:
        model = pickle.load(file)

    # Perform inference or further operations with the loaded model
    #predictions = loaded_model.predict(X_test)
    testx,testy=split(n_steps,data[i])
    testX.append(testx)
    testY.append(testy)
    test_predict=model.predict(testX[i])
    Test_Predict.append(test_predict)
    print(test_predict)
    Scaled_testPredict = Scalers[i].inverse_transform(Test_Predict[i])
    Scaled_testY = Scalers[i].inverse_transform(testY[i])

    testY_flat=Scaled_testY.reshape(-1)
    plt.plot(testY_flat)
    testPredict_flat=Scaled_testPredict.reshape(-1)
    predictions[phase] = testPredict_flat
    plt.plot(testPredict_flat)
    plt.legend('Ground Turth','Prediction')
    plt.legend(loc="upper left")

    plt.show()

    plt.figure(figsize=(10, 5))

    plt.plot(Scaled_testY[:48],label="Ground Turth")
    plt.plot(testPredict_flat[:48],label="Prediction")
    #plt.xlabel('Hours')
    plt.ylabel('Traffic')
    plt.legend(loc="upper left")

    plt.show()

    print(model.summary())

    print('Test')
    model_eval.mae(Scaled_testY,testPredict_flat)
    model_eval.mse(Scaled_testY,testPredict_flat)
    model_eval.rmse(Scaled_testY,testPredict_flat)

print(predictions)
