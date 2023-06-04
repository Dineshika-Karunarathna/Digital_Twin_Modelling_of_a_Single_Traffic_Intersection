from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error
from math import sqrt



def mae(Scaled_trainY,trainPredict_flat):
    mae = mean_absolute_error(Scaled_trainY, trainPredict_flat)
    print('MAE: %f' % mae)
    return mae
def mse(Scaled_trainY,trainPredict_flat):
    mse = mean_squared_error(Scaled_trainY, trainPredict_flat)
    print('MSE: %f' % mse)
    return mse
def rmse(Scaled_trainY,trainPredict_flat) :   
    rmse = sqrt(mean_squared_error(Scaled_trainY, trainPredict_flat))
    print('RMSE: %f' % rmse)
    return rmse


# mse = mean_squared_error(Scaled_trainY, trainPredict_flat)
# print('MSE: %f' % mse)
# rmse = sqrt(mse)
# print('RMSE: %f' % rmse)