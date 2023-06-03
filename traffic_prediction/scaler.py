from sklearn.preprocessing import MinMaxScaler


def scale_data(dataset):
    scaler = MinMaxScaler(feature_range=(0, 1)) #Also try QuantileTransformer
    dataset = scaler.fit_transform(dataset)
    return dataset

def inverse_scale_data(dataset):
    scaler = MinMaxScaler(feature_range=(0, 1)) #Also try QuantileTransformer
    dataset = scaler.inverse_transform(dataset)
    return dataset