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
N_S=traffic_data[['N_S']].values
N_S=traffic_data[['N_S']].values
N_W=traffic_data[['N_W']].values
S_N=traffic_data[['S_N']].values
S_W=traffic_data[['S_W']].values
W_N=traffic_data[['W_N']].values
W_S=traffic_data[['W_S']].values
scaler1 = MinMaxScaler(feature_range=(0, 1))
N_S = scaler1.fit_transform(N_S)






##############################################################################################






print(N_S )
print(len(N_S))



plt.plot(N_S)
plt.show()





n_steps=39
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
models=[]
Train_Predict=[]
Test_Predict=[]

trainx,trainy,testx,testy=split(n_steps,N_S)
trainX.append(trainx)
trainY.append(trainy)
testX.append(testx)
testY.append(testy)
model=lstm_mod.stacked_train(learning_rate, batch_size ,epochs,n_steps,n_features,trainX[0],trainY[0])

models.append(model)
print(trainX[0].shape)
print(model.summary())



# trainX,trainY,testX,testY=split(n_steps,N_S)
# model=lstm_mod.stacked_train(learning_rate, batch_size ,epochs,n_steps,n_features,trainX,trainY)
train_predict=model.predict(trainX[0])
print("train Predict")
print(train_predict.shape)
print(train_predict)
Train_Predict.append(train_predict)
test_predict=model.predict(testX[0])
Test_Predict.append(test_predict)
print(test_predict)

Scaled_trainPredict = scaler1.inverse_transform(Train_Predict[0])
Scaled_trainY = scaler1.inverse_transform(trainY[0])
Scaled_testPredict = scaler1.inverse_transform(Test_Predict[0])
Scaled_testY = scaler1.inverse_transform(testY[0])

trainY_flat=Scaled_trainY.reshape(-1)
plt.plot(trainY_flat)

trainPredict_flat=Scaled_trainPredict.reshape(-1)
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

plt.plot(Scaled_testY[:48],label="Ground Turth")
plt.plot(testPredict_flat[:48],label="Prediction")
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