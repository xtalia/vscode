import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

__location__ = os.path.dirname(os.path.abspath(__file__))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_questions(link):
    if link == "111":
        debug_xml_path = os.path.join(__location__, 'debug.xml')
        
        with open(debug_xml_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, "xml")
            return soup.find_all('item')

    parsed_url = urlparse(link)
    atl = parse_qs(parsed_url.query)['object_id'][0]
    code = parse_qs(parsed_url.query)['part_code'][0]

    url = f"https://abc.tele2.ru/qti_return.html?atl={atl}&code={code}&charset=utf-8"
    print(url)
    
    response = requests.get(url)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, "xml")
    return soup.find_all('item')

def print_question_and_answers(qss):
    counter = 0
    for qs in qss:
        counter += 1
        title = qs.get('title')
        print(f"\n<{counter}> {title}\n")
        
        ass = qs.find('response_lid')
        meme = ass.find_all("response_label", {"ws_right": "1"})
        
        for sas in meme:
            mattext_text = sas.find('mattext').text
            print(f">> {mattext_text}")

def start():
    print("sergsinist webtutor answer crawler")
    start = input("Вставьте ссылку теста из браузера, где есть кнопка начать\продолжить тест: ")
    
    while start.strip():
        questions = fetch_questions(start)
        print_question_and_answers(questions)
        
        start = input("Можете повторить или нажать Enter для выхода: ")
        clear_screen()
    else:
        quit()

if __name__ == "__main__":
    start()
