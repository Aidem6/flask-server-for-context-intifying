from flask import Flask, jsonify, request
app = Flask(__name__)


accelerometerData = [
    {
        "activity": 1,
        "time_s": 641.13,
        "a_x": 0.328,
        "a_y": 1.07,
        "a_z": -0.285,
    }
]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/incomes')
def get_incomes():
    return jsonify(accelerometerData)


@app.route('/incomes', methods=['POST'])
def add_income():
    accelerometerData.append(request.get_json())
    return '', 204