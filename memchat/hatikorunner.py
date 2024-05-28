from flask import Flask, request, jsonify
from who_work import get_employee_info
from wr_tradein import calculate_ideal_price
from flask_cors import CORS
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

@app.route('/who_work', methods=['GET'])
def who_work():
    day = request.args.get('day')
    text = get_employee_info(day)
    return jsonify({'text': text})

@app.route('/tradein', methods=['GET'])
def tradein():
    # Извлекаем параметры из запроса и декодируем пробелы
    model = unquote(request.args.get('model', ''))
    memory = unquote(request.args.get('memory', ''))
    battery_capacity = int(request.args.get('battery_capacity', 0))
    package = unquote(request.args.get('package', ''))
    back_cover = request.args.get('back_cover', type=bool, default=False)
    screen = request.args.get('screen', type=bool, default=False)
    condition = unquote(request.args.get('condition', ''))

    # Вызываем функцию для расчета идеальной цены
    ideal_price = calculate_ideal_price(
        model,
        memory,
        battery_capacity,
        package,
        back_cover,
        screen,
        condition
    )

    # Возвращаем JSON-ответ с идеальной ценой
    return jsonify({'ideal_price': ideal_price})
    
if __name__ == '__main__':
    app.run(debug=True)