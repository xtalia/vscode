from flask import Flask, request, jsonify
from who_work import get_employee_info
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/who_work', methods=['GET'])
def who_work():
    day = request.args.get('day')
    text = get_employee_info(day)
    return jsonify({'text': text})
    
if __name__ == '__main__':
    app.run(debug=True)