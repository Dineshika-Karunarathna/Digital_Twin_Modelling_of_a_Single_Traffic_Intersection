from numpy import array
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import file_handler
import scale
import split_data
import lstm_mod
import model_eval
import os



import pandas as pd
from sklearn.preprocessing import MinMaxScaler


traffic_data = pd.read_csv('D:\\Acedamic\\FYP\\Codes\\Datasets\\3_way.csv')
traffic_data.dropna(inplace=True)
traffic_data = traffic_data.drop(columns=['Frame', '5 Minute'])
'''
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(traffic_data.values)
scaled_traffic_data = pd.DataFrame(scaled_data, columns=traffic_data.columns)
print(type(scaled_traffic_data))

'''
data=[]
for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
    data.append(traffic_data[phase].values)


# N_S=traffic_data[['N_S']].values
#N_W=traffic_data[['N_W']].values
# S_N=traffic_data[['S_N']].values
# S_W=traffic_data[['S_W']].values
# W_N=traffic_data[['W_N']].values
# W_S=traffic_data[['W_S']].values  
#print(N_W)
Scalers=[]
for i in range(6):
    Scalers.append(MinMaxScaler(feature_range=(0, 1)))
# scaler1 = MinMaxScaler(feature_range=(0, 1))
# scaler2 = MinMaxScaler(feature_range=(0, 1))
# scaler3 = MinMaxScaler(feature_range=(0, 1))
# scaler4 = MinMaxScaler(feature_range=(0, 1))
# scaler5 = MinMaxScaler(feature_range=(0, 1))
# scaler6 = MinMaxScaler(feature_range=(0, 1))
print(Scalers[0])

for i in range(6):
    data[i]=Scalers[i].fit_transform(data[i].reshape(-1,1))
# N_S = scaler1.fit_transform(data[0].reshape(-1,1))
# N_W = scaler2.fit_transform(data[1].reshape(-1,1))
# S_N = scaler3.fit_transform(data[2].reshape(-1,1))
# S_W = scaler4.fit_transform(data[3].reshape(-1,1))
# W_N = scaler5.fit_transform(data[4].reshape(-1,1))
# W_S = scaler6.fit_transform(data[5].reshape(-1,1))








##############################################################################################


N_S=data[0]



print(N_S )
print(len(N_S))



plt.plot(N_S)
plt.show()





n_steps=37
n_features = 1

def split(n_steps,dataset):

    train_size = int(len(dataset) * 0.66)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
    trainX, trainY = split_data.split_sequence(train, n_steps)
    testX, testY = split_data.split_sequence(test, n_steps)

    print(trainX.shape, trainY.shape)
    print(testX.shape, testY.shape)


    # define input sequence
    #raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    # choose a number of time steps
    
    # split into samples
    X, y = split_data.split_sequence(dataset, n_steps)
    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    print(trainX.shape, trainY.shape)
    print(testX.shape, testY.shape)
    trainX = trainX.reshape((trainX.shape[0], trainX.shape[1], n_features))
    testX = testX.reshape((testX.shape[0], testX.shape[1], n_features))
    print(trainX.shape, trainY.shape)
    print(testX.shape, testY.shape)

    testY_flat=testY.reshape(-1)
    plt.plot(testY_flat)
    plt.show()
    return trainX,trainY,testX,testY

learning_rate = 0.06
batch_size = 8
epochs=2

trainX=[]
trainY=[]
testX=[]
testY=[]
models = {}
predictions = {}
Train_Predict=[]
Test_Predict=[]
for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
    trainx,trainy,testx,testy=split(n_steps,data[i])
    trainX.append(trainx)
    trainY.append(trainy)
    testX.append(testx)
    testY.append(testy)

#folder_path = '\Models\weights'
folder_path = 'D:\Acedamic\FYP\Codes\DTMSTI\Digital_Twin_Modelling_of_a_Single_Traffic_Intersection\\traffic_prediction\Models\weights'

os.makedirs(folder_path, exist_ok=True)

for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
    model=lstm_mod.stacked_train(learning_rate, batch_size ,epochs,n_steps,n_features,trainX[i],trainY[i])
    models[phase] = model

    filename = f'model_{i}.pkl'
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)




    print(trainX[i].shape)
    print(model.summary())
    train_predict=model.predict(trainX[i])
    print("train Predict")
    print(train_predict.shape)
    print(train_predict)
    Train_Predict.append(train_predict)
    test_predict=model.predict(testX[i])
    Test_Predict.append(test_predict)
    print(test_predict)

    Scaled_trainPredict = Scalers[i].inverse_transform(Train_Predict[i])
    Scaled_trainY = Scalers[i].inverse_transform(trainY[i])
    Scaled_testPredict = Scalers[i].inverse_transform(Test_Predict[i])
    Scaled_testY = Scalers[i].inverse_transform(testY[i])


    trainY_flat=Scaled_trainY.reshape(-1)
    plt.plot(trainY_flat)

    trainPredict_flat=Scaled_trainPredict.reshape(-1)
    predictions[phase] = trainPredict_flat
    plt.plot(trainPredict_flat)
    plt.legend('Ground Turth','Prediction')
    plt.show()


    plt.figure(figsize=(10, 5))
    plt.plot(Scaled_trainY[:48], label="Ground Turth")
    plt.plot(trainPredict_flat[:48],label="Prediction")
    plt.legend(loc="upper left")

    plt.show()

    testY_flat=Scaled_testY.reshape(-1)
    plt.plot(testY_flat)
    testPredict_flat=Scaled_testPredict.reshape(-1)
    plt.plot(testPredict_flat)
    plt.legend('Ground Turth','Prediction')
    plt.legend(loc="upper left")

    plt.show()

    plt.figure(figsize=(10, 5))

    plt.plot(Scaled_testY[:38],label="Ground Turth")
    plt.plot(testPredict_flat[:38],label="Prediction")
    #plt.xlabel('Hours')
    plt.ylabel('Traffic')
    plt.legend(loc="upper left")

    plt.show()

    print(model.summary())

    print('Train')
    model_eval.mae(Scaled_trainY,trainPredict_flat)
    model_eval.mse(Scaled_trainY,trainPredict_flat)
    model_eval.rmse(Scaled_trainY,trainPredict_flat)
    print('Test')
    model_eval.mae(Scaled_testY,testPredict_flat)
    model_eval.mse(Scaled_testY,testPredict_flat)
    model_eval.rmse(Scaled_testY,testPredict_flat)


        









    # trainX,trainY,testX,testY=split(n_steps,N_S)
    # model=lstm_mod.stacked_train(learning_rate, batch_size ,epochs,n_steps,n_features,trainX,trainY)


print(predictions['N_S'])
print(predictions['N_W'])




