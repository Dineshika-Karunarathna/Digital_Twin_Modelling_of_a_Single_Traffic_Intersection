import gspread_connection
import pandas as pd

client=gspread_connection.connect()
gspread_connection.create_sheet(client)

data=gspread_connection.get_data(client)
print(data)