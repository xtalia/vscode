import os

# Путь к директории, содержащей main.py
directory = os.path.dirname(os.path.abspath(__file__))

# Получение списка файлов в директории
files = os.listdir(directory)

# Отфильтровать только файлы с расширением .py
python_files = [file for file in files if file.endswith('.py')]

# Вывод списка файлов
file_list = '\n'.join(python_files)
print(f"Список модулей:\n{file_list}")