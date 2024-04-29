import streamlit as st
import json

# Initialize an empty dictionary to store the data
data = {}

def load_data():
    with open('test.json', 'r') as f:
        global data
        data = json.load(f)
    st.experimental_rerun()

def save_data():
    with open('test.json', 'w') as f:
        json.dump(data, f)
    st.experimental_rerun()

def edit_json():
    for key, value in data.items():
        st.write(f"{key}: {value}")

    new_entry = st.text_input("New Entry:")
    if new_entry:
        data[new_entry] = "value"
        with open('test.json', 'w') as f:
            json.dump(data, f)

    for key in data.keys():
        st.write(f"{key}:")
        new_value = st.text_input("New Value:")
        if new_value:
            data[key] = new_value
            with open('test.json', 'w') as f:
                json.dump(data, f)
                
def run_editor():
    st.title("JSON Editor")
    edit_json()
    st.button("Save", on_click=save_data)
    st.button("Load", on_click=load_data)

if __name__ == '__main__':
    run_editor()