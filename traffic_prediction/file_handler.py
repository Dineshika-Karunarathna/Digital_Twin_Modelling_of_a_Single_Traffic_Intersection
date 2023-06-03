import os
import pandas as pd

def get_file_path(file_name):
    """Returns the file path of the given file name."""
    return os.path.join(os.path.dirname(__file__), file_name)

def get_file_content(file_name):

    """Returns the content of the given file name."""
    with open(get_file_path(file_name), 'r') as file:
        return file.read()
def read_data(file_name):
    """Returns the content of the given file name."""
    with open(get_file_path(file_name), 'r') as file:
        return file.read()
def write_data(file_name, data):
    """Writes the given data to the given file name."""
    with open(get_file_path(file_name), 'w') as file:
        file.write(data)
def get_data(file_name):
    """Returns the content of the given file name."""
    with open(get_file_path(file_name), 'r') as file:
        traffic_data = pd.read_csv(file)
        dataset=traffic_data.values
        #dataset=dataset.astype('float32')

    return dataset