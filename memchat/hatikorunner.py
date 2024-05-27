from flask import Flask, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime, timedelta
import config  # Создайте config.py для хранения конфигурационных данных

app = Flask(__name__)

WW_LINK = config.WW_LINK
WW_PLACES = config.WW_PLACES

def get_google_sheets_data(day_offset):
    cred_json = config.cred_json
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(WW_LINK)
    worksheet = sheet.get_worksheet(0)

    day = datetime.now().day + day_offset

    values_a = worksheet.col_values(1)[3:]
    values_b = worksheet.col_values(1 + day)[3:]

    employee_info = []
    for a, b in zip(values_a, values_b):
        if a and a.startswith('!'):
            employee_info.append(f"\n🏢 В городе: {a[1:]}{b}\n")
        elif b and b != '':
            a = WW_PLACES.get(a, a)
            b = WW_PLACES.get(b, b)
            employee_info.append(f"👤 {a}: {b}")

    return employee_info

@app.route('/who_work', methods=['GET'])
def who_work():
    day = request.args.get('day')
    day_offset = 0 if day == 'today' else 1
    day_text = 'Сегодня' if day_offset == 0 else 'Завтра'

    employee_info = get_google_sheets_data(day_offset)
    if employee_info:
        text = f"{day_text} ({(datetime.now() + timedelta(days=day_offset)).strftime('%d.%m.%Y')}) работают:\n" + '\n'.join(employee_info)
    else:
        text = f"{day_text} ({(datetime.now() + timedelta(days=day_offset)).strftime('%d.%m.%Y')}) никто не работает"

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
