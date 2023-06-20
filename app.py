from flask import Flask, jsonify, request
import random

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

# run_algorithm(whichAlgorithm, accelerometerData):

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/accelerometerData', methods=['GET'])
def get_incomes():
    return jsonify(accelerometerData)

@app.route('/accelerometerData', methods=['POST'])
def add_income():
    accelerometerData.append(request.get_json())
    return jsonify('Successfully appended data')

@app.route('/identifyContext', methods=['POST'])
def identify_context():
    whichAlgorithm = request.get_json()['whichAlgorithm']
    accelerometerData = request.get_json()['accelerometerData']
    data = {
        "status": "success",
        "whichAlgorithm": whichAlgorithm,
        "accelerometerData": accelerometerData,
        "result": random.choice(["walking", "driving", "cycling"]),
        "confidence": random.randrange(60, 94, 1) / 100.0,
        "time_needed": random.randrange(10, 40, 1) / 100.0
    }
    return jsonify(data)