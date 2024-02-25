import streamlit as st
import index
from as_calculator import cash_amount, original_price
from avitoplag import find_models
import os
import config as cf


st.set_page_config(
    page_title="Мемный Чат",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.header('Мемный Чат', divider='violet')
st.header('_Streamlit_ is :blue[cool] :sunglasses:')

# Создаем три вкладки: Анализ данных, Визуализация и Машинное обучение
tab1, tab2, tab3 = st.tabs(["Трейдин", "Калькуляторы", "Avito Классификатор"])

# В первой вкладке вызываем функцию из модуля tab1
with tab1:
    index.analyze_data()

with tab2:
    cash_amount()
    st.divider()
    original_price()
    
with tab3:
    # Вызываем функцию find_models с нужными аргументами и получаем результат
    model = st.text_input("Введите модель (например 15 Pro)", value="15 pro")
    found_models = find_models(os.path.join(cf.dir_path, 'phones.xml'), model)

    # Проверяем, найдены ли модели
    if found_models:
        # Выводим заголовок с количеством найденных моделей
        st.header(f"Найдено {len(found_models)} моделей")
        # Выводим данные в виде таблицы
        st.dataframe(found_models)
    else:
        # Выводим сообщение, что модели не найдены
        st.write("Модели не найдены")
