# Используем официальный Python-runtime в качестве родительского образа
FROM python:3

# Копируем файлы проекта в рабочую директорию контейнера
COPY . /app

# Указываем рабочую директорию
WORKDIR /app

ENV DEBUG=False

# Устанавливаем зависимости
RUN pip3 install -r requirements.txt

# Запускаем основной файл приложения
CMD ["python3", "main.py"]