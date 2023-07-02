import gspread
import json
import os
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

if __name__ == '__main__':
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

  day = datetime.now().day

  # get values from the 1st, 2nd, and 3rd columns, starting from row 4
  values_a = worksheet.col_values(1)[3:]
  values_b = worksheet.col_values(1 + day)[3:]
  values_c = worksheet.col_values(2 + day)[3:]

  # print(values_a)
  # print(values_b)
  # print(values_c)
        
  # create a dictionary for replacement
  replace_dict = {
      'У': 'Как Управляющий',
      'М': 'Как Менеджер',
      'РБ': 'в ТЦ Рубин',
      'Р': 'на Рахова',
      'К': 'на Казачьей',
      'Ч': 'на Чернышевского'
  }

  # get the current date and time
  now = datetime.now()

  # print the values from the 1st and 2nd columns
  a_values = []
  for a, b in zip(values_a, values_b):
      if a is not None:
          if a.startswith('!'):
              a_values.append(f"\n🏢 В городе: {a[1:]}{b}\n")
          elif b is not None and b != '':
              a = replace_dict.get(a, a)
              b = replace_dict.get(b, b)
              a_values.append(f"👤 {a}: {b}")

  # format the output
  if a_values:
      print(f"Сегодня ({now.strftime('%d.%m.%Y')}) работают:\n" + '\n'.join(a_values))
  else:
      print(f"Сегодня ({now.strftime('%d.%m.%Y')}) никто не работает")