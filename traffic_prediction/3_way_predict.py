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
import time



def split(n_steps,dataset):
    n_features=1
    testX, testY = split_data.split_sequence(dataset, n_steps)
    testX = testX.reshape((testX.shape[0], testX.shape[1], n_features))
    testY_flat=testY.reshape(-1)
    plt.plot(testY_flat)
    plt.show()
    return testX,testY

def predict_all():
    testX=[]
    testY=[]
    Test_Predict=[]
    predictions={}

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

    n_steps=37
    n_features = 1


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

        plt.plot(Scaled_testY[:39],label="Ground Turth")
        plt.plot(testPredict_flat[:39],label="Prediction")
        #plt.xlabel('Hours')
        plt.ylabel('Traffic')
        plt.legend(loc="upper left")

        plt.show()

        print(model.summary())

        print('Test')
        model_eval.mae(Scaled_testY,testPredict_flat)
        model_eval.mse(Scaled_testY,testPredict_flat)
        model_eval.rmse(Scaled_testY,testPredict_flat)

    print(type(predictions['N_S']))
    df = pd.DataFrame(predictions)
    df.to_csv('output.csv', index=True)





def read_last_10_rows():
    
    
    df = pd.read_csv('D:\\Acedamic\\FYP\\Codes\\Datasets\\3_way.csv')
    df.dropna(inplace=True)
    df = df.drop(columns=['Frame', '5 Minute'])
    last_10_rows = df.tail(37)
    return last_10_rows




# Read the last 10 rows of the CSV file periodically







def future_10_process(last_10_rows):
    last_10 = []
    predictions_10 = []
    predictions={}

    data=[]
    for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
        data.append(last_10_rows[phase].values)
    
    
    Scalers=[]
    for i in range(6):
        Scalers.append(MinMaxScaler(feature_range=(0, 1)))

    for i in range(6):
        data[i]=Scalers[i].fit_transform(data[i].reshape(-1,1))
        
    folder_path = 'D:\Acedamic\FYP\Codes\DTMSTI\Digital_Twin_Modelling_of_a_Single_Traffic_Intersection\\traffic_prediction\Models\weights'

    for i, phase in enumerate(['N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S']):
        filename = f'model_{i}.pkl'
        file_path = os.path.join(folder_path, filename)
    
        with open(file_path, 'rb') as file:
            model = pickle.load(file)
        
        last_10 = data[i]
        for j in range(10):
            last_prediction=model.predict(last_10)
            predictions_10.append(last_prediction)
            np.append(last_10,last_prediction)
            last_10 = last_10[1:]

        print(predictions_10)
        print(predictions_10.shape)
        print(predictions_10[0].shape)
        print(predictions_10[0])
        print(last_prediction)
        

        Scaled_predictions_10 = Scalers[i].inverse_transform(predictions_10)
        Scaled_predictions_10_flat=Scaled_predictions_10.reshape(-1)
        plt.plot(Scaled_predictions_10_flat)
        predictions[phase] = Scaled_predictions_10_flat
        print(predictions[phase])



    
    
def future_10_start(predictions):
    while True:
        last_10_rows = read_last_10_rows('D:\\Acedamic\\FYP\\Codes\\Datasets\\3_way.csv')
        print(last_10_rows)
   
    
        time.sleep(300)  
    return 0
    

def test():
    future_10_process(read_last_10_rows())
    return 'Done'
test()
#predict_all()

    


    
    