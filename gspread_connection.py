import gspread
from oauth2client.service_account import ServiceAccountCredentials



def connect():
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    print('Connected to Google Sheets!')
    return client

    
def create_sheet(client):
    
    sheet = client.open('Vehicle_Counts')
    #worksheet = sheet.add_worksheet(title="Prediction", rows=200, cols=20)
    worksheet = sheet.worksheet("Prediction")
    worksheet.clear()
    worksheet.insert_row([ '5 Minute', 'N_S', 'N_W', 'S_N', 'S_W', 'W_N', 'W_S'], 1)
    print('Sheet Created!')
    return worksheet

def get_data(client):
    sheet = client.open('Vehicle_Counts')
    worksheet = sheet.worksheet("Camera_Data")
    data = worksheet.get_all_values()
    print('Data Fetched!')
    return data




def insert_row(worksheet, row):
    worksheet.insert_row(row, 2)
    print('Row Inserted!')
    return worksheet

def update_cell(worksheet, row, col, value):
    worksheet.update_cell(row, col, value)
    print('Cell Updated!')
    return worksheet
def update_row(worksheet, row, value):
    worksheet.update_row(row, value)
    print('Row Updated!')
    return worksheet
def update_column(worksheet, col, value):
    worksheet.update_column(col, value)
    print('Column Updated!')
    return worksheet
def get_cell(worksheet, row, col):

    cell = worksheet.cell(row, col).value
    print('Cell Fetched!')
    return cell
def get_row(worksheet, row):
    row = worksheet.row_values(row)
    print('Row Fetched!')
    return row
def get_column(worksheet, col):
    column = worksheet.col_values(col)
    print('Column Fetched!')
    return column
def get_range(worksheet, row1, col1, row2, col2):
    range = worksheet.range(row1, col1, row2, col2)
    print('Range Fetched!')
    return range
def update_range(worksheet, row1, col1, row2, col2, values):
    cell_list = worksheet.range(row1, col1, row2, col2)
    for cell, value in zip(cell_list, values):
        cell.value = value
    worksheet.update_cells(cell_list)
    print('Range Updated!')
    return worksheet
def get_all(worksheet):

    list_of_lists = worksheet.get_all_values()
    print('All Fetched!')
    return list_of_lists
def get_all_records(worksheet):
    list_of_dicts = worksheet.get_all_records()
    print('All Fetched!')
    return list_of_dicts
def get_worksheet(client, name):
    sheet = client.open('Vehicle_Counts')
    worksheet = sheet.worksheet(name)
    print('Worksheet Fetched!')
    return worksheet

