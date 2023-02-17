import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds=ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client=gspread.authorize(creds)
sheet=client.open('Vehicle_Counts')
print(sheet.get_all_records())
