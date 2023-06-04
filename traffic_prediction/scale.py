from sklearn.preprocessing import MinMaxScaler
#scaler = MinMaxScaler(feature_range=(0, 1))

def scale_data(dataset,scaler):
     #Also try QuantileTransformer
    #scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    return dataset

def inverse_scale_data(dataset,scaler):
    #scaler = MinMaxScaler(feature_range=(0, 1)) #Also try QuantileTransformer
    dataset = scaler.inverse_transform(dataset)
    return dataset