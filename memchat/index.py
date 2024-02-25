import streamlit as st
import os
import json
import config as cf
import tradeinloader



# Загружаем файл с данными
with open(os.path.join(cf.dir_path, 'data.json'), 'r') as f:
    data = json.load(f)

# Получаем список моделей из ключей словаря
models = list(data.keys())



# Создаем функцию для анализа данных
def analyze_data():

    result = ""
    

    
    # Позволяем пользователю выбрать модель из выпадающего списка
    model = st.selectbox("Выберите модель", models) 
    
    # Получаем список вариантов памяти для выбранной модели
    memory_options = [item["memory"] for item in data[model]] 
    
    # Позволяем пользователю выбрать память из выпадающего списка
    memory = st.selectbox("Выберите память", memory_options) 
    
    # Находим соответствующий словарь с параметрами для выбранной модели и памяти
    params = next(item for item in data[model] if item["memory"] == memory) 
    
    # Получаем идеальную цену из словаря
    ideal_price = int(params["ideal_price"]) 

    col1, col2 = st.columns(2)
    
    # Позволяем пользователю выбрать емкость аккумулятора с помощью слайдера
    battery_capacity = col2.slider("Емкость аккумулятора", 0, 100, value=99)
    

    # Если емкость меньше 85, прибавляем стоимость замены аккумулятора
    if battery_capacity < 85:
        ideal_price += int(params["battery_replacement"])
    # Если емкость от 85 до 90, прибавляем стоимость износа аккумулятора
    elif 85 <= battery_capacity < 90:
        ideal_price += int(params["battery_wear"])
        

    package = col2.selectbox("Выберите комплектацию", ["Только устройство", "Устройство + коробка", "Полный"]) 
    
    # Позволяем пользователю выбрать комплектацию из выпадающего списка

    # Если выбрано только устройство, прибавляем стоимость отсутствия коробки и аксессуаров
    if package == "Только устройство":
        ideal_price += int(params["device_only"])
    # Если выбрано устройство + коробка, прибавляем стоимость отсутствия аксессуаров
    elif package == "Устройство + коробка":
        ideal_price += int(params["device_box"])


    # Позволяем пользователю выбрать целостность задней крышки из выпадающего списка
    back_cover = col2.toggle(" Требуется **замена крышки** (очень сильно разбито, отсутствуют элементы)")

    # Если выбрано нет, прибавляем стоимость замены задней крышки
    if back_cover:
        ideal_price += int(params["back_cover_replacement"])
        result += (f"🏥 Требуется замена крышки  \n")

    # Позволяем пользователю выбрать целостность экрана из выпадающего списка
    screen = col2.toggle("Требуется **замена экрана** (ошибка в настройках, разбит, отсутствуют элементы)")

    # Если выбрано нет, прибавляем стоимость замены экрана
    if screen:
        ideal_price += int(params["screen_replacement"])
        result += (f"🏥 Требуется замена экрана  \n")

    # Позволяем пользователю выбрать внешнее состояние из выпадающего списка
    
    condition = col2.select_slider("Выберите внешнее состояние", value="😎 Отличное",  options= ["😢 Плохое", "😐 Среднее", "😀 Хорошее", "😎 Отличное"])

    # Если выбрано среднее, прибавляем стоимость потертостей
    if condition == "😐 Среднее":
        # Если идеальная цена меньше 20000, прибавляем -2000
        if ideal_price < 20000:
            ideal_price -= 2000
        # Иначе прибавляем -1000
        else:
            ideal_price -= 1000
    # Если выбрано плохое, прибавляем стоимость повреждений
    elif condition == "😢 Плохое":
        # Если идеальная цена меньше 20000, прибавляем -3000
        if ideal_price < 20000:
            ideal_price -= 3000
        # Иначе прибавляем -2000
        else:
            ideal_price -= 2000

    # Выводим итоговую цену
    
    result += (f"📲 {model} на {memory}  \n")
    result += (f"🔋Аккумулятор {battery_capacity}%  \n")
    result += (f"📦 Комплект {package}  \n")
    if back_cover == False and screen == False: result += (f"✅ Экран и задняя крышка не требуют замены  \n")
    result += (f"{condition}  состояние  \n")
    
    
    col1.write(result)
    col1.write(f"**💰Предварительная цена выкупа**: {ideal_price} рублей")
    col1.write("👉 ‍‍Окончательная стоимость будет известна только при непосредственной проверке в магазине")
    
    # Добавляем кнопку "обновить цены" с текстом "Обновить"
    update_button = st.button("⚠️ Обновить данные с таблицы")

    # Если пользователь нажал на кнопку, запускаем функцию из модуля kekjpeg
    if update_button:
        with st.spinner('Обновляем информацию'):
            tradeinloader.load()
