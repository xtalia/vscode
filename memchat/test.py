import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# define the scope of the API client
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# authenticate the API client
dir_path = os.path.dirname(os.path.realpath(__file__))
creds = ServiceAccountCredentials.from_json_keyfile_name(dir_path + '\creds.json', scope)
client = gspread.authorize(creds)

# open the Google Sheets document by URL
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/13KUmHtRXYbXjBE7KQ_4MFQ5VsgUYqu2heURY1y2NwiE/edit#gid=0')

# select the worksheet by index (0-indexed)
worksheet = sheet.get_worksheet(0)

# get all values from the worksheet as a list of lists
data = worksheet.get_all_values()

# print the data
print(data)