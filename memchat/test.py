import os
import sys
import locale
new_locale = os.getenv('PYTHON_LOCALE', 'ru_RU.UTF-8')
locale.setlocale(locale.LC_ALL, new_locale)


preferred_encoding = locale.getpreferredencoding()
print(sys.getdefaultencoding())
print(preferred_encoding)

import json

with open('settings.json', 'r') as json_file:
    data = json.load(json_file)

WW_LINK = data.get('WW_LINK')
print(WW_LINK)