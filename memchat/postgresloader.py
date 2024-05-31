from config import config_data as creds
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import time
from threading import Timer

DB_LOGIN = creds["db"]["login"]
DB_PASS = creds["db"]["pass"]
DB_HOST = creds["db"]["host"]
DB = creds["db"]["db"]


# Cache to hold the data
cache_file = 'cache.json'
last_updated = 0
cache_duration = 30 * 60  # 30 minutes

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB,
        user=DB_LOGIN,
        password=DB_PASS
    )

def load_cache():
    global cache, last_updated
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
            cache = data['cache']
            last_updated = data['last_updated']
    except (FileNotFoundError, json.JSONDecodeError):
        cache = None
        last_updated = 0

def save_cache():
    global cache, last_updated
    with open(cache_file, 'w') as f:
        json.dump({'cache': cache, 'last_updated': last_updated}, f)

def map_to_english(item):
    return {
        'article': item['Артикул'],
        'external_code': item['Внешний код'],
        'name': item['Наименование'],
        'competitor_shop': item['Магазин конкурент'],
        'competitor_price': item['Цена конкурента'],
        'store_saratov': item['Магазин Саратов'],
        'store_voronezh': item['Магазин Воронеж'],
        'store_lipetsk': item['Магазин Липецк'],
        'store_balakovo': item['Магазин Балаково'],
        'price_saratov': item['Цена: Саратов'],
        'price_voronezh': item['Цена: Воронеж'],
        'price_lipetsk': item['Цена: Липецк'],
        'price_balakovo': item['Цена: Балаково'],
        'recommended_saratov': item['Рекомендуемая Саратов'],
        'recommended_voronezh': item['Рекомендуемая Воронеж'],
        'recommended_lipetsk': item['Рекомендуемая Липецк'],
        'recommended_balakovo': item['Рекомендуемая Балаково']
    }

def update_cache(force=False):
    global cache, last_updated
    if not force and (time.time() - last_updated < cache_duration):
        return
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM table_bots')
        data = cur.fetchall()
        cache = [map_to_english(item) for item in data]
        cur.close()
        conn.close()
        last_updated = time.time()
        save_cache()
        print("Cache updated")
    except Exception as e:
        print(f"Error updating cache: {e}")
        if cache is None:
            raise

# Automatically update the cache every 44 minutes
def schedule_cache_update():
    Timer(cache_duration, schedule_cache_update).start()
    update_cache()

# Initial cache load and update
load_cache()
update_cache()
schedule_cache_update()

def search_cache(query):
    if isinstance(query, str):
        return [item for item in cache if query.lower() in item["name"].lower()][:5]
    elif isinstance(query, int):
        return next((item for item in cache if item["article"] == str(query)), None)
    return []

def format_response(item):
    if not item:
        return "No data found"

    template = f"""
🆔 {item['article']}
🔢 {item['external_code']}
🏷️ {item['name']}
💰 🆂: {item['price_saratov']} {'😀' if item['price_saratov'] >= item['recommended_saratov'] else '😢 не проходим'} 
💰 🆅: {item['price_voronezh']} {'😀' if item['price_voronezh'] >= item['recommended_voronezh'] else '😢 не проходим'} 
💰 🅻: {item['price_lipetsk']} {'😀' if item['price_lipetsk'] >= item['recommended_lipetsk'] else '😢 не проходим'} 
💰 🅱️: {item['price_balakovo']} {'😀' if item['price_balakovo'] >= item['recommended_balakovo'] else '😢 не проходим'} 
💖 Рекомендуемые цены: 🆂 {item['recommended_saratov']}, 🆅 {item['recommended_voronezh']}, 🅻 {item['recommended_lipetsk']}, 🅱️ {item['recommended_balakovo']}
📦 Есть: 🆂 {item['store_saratov']}, 🆅 {item['store_voronezh']}, 🅻 {item['store_lipetsk']}, 🅱️ {item['store_balakovo']}
Отдаем? Сможете привезти?
"""
    return template.strip()

def handle_query(query):
    try:
        update_cache()
    except Exception as e:
        if isinstance(query, int):
            return f"Server error: {e}. Try again later."
        else:
            return "Server error, send the request as a number and contact Ivan."

    if isinstance(query, str) and not query.isdigit():
        results = search_cache(query)
        if not results:
            return "No data found"
        return "\n\n".join([format_response(item) for item in results])
    elif query.isdigit():
        result = search_cache(int(query))
        if result:
            return format_response(result)
        else:
            return "No data found"
    else:
        return "Invalid query"

# Example usage
if __name__ == "__main__":

    while True:
        query = input("Enter search query (text or article number): ")
        print(handle_query(query))
