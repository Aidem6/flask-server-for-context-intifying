from flask import Flask, jsonify, request
import random
from keras.models import load_model
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import math
from statistics import mean
import time


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

model = load_model('trained_cnn_model.h5')

def preprocess_data(X_test):
    # Reshape the data
    n_samples, n_timesteps, n_features = X_test.shape
    X_test_flattened = X_test.reshape((n_samples, n_timesteps * n_features))

    # Apply standardization to the data
    scaler = StandardScaler()
    X_test_scaled = scaler.transform(X_test_flattened)

    # Apply normalization to the data
    normalizer = MinMaxScaler()
    X_test_norm = normalizer.transform(X_test_scaled)

    # Reshape the data back to 3D
    n_samples, n_timesteps, n_features = X_test.shape
    X_test_norm = X_test_norm.reshape((n_samples, n_timesteps, n_features))

    return X_test_norm

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

@app.route('/evaluateCNNModel', methods=['POST'])
def evaluate_model():
    accelerometerData = np.array(request.get_json()['accelerometerData'])
    fullHoundreds = math.floor(accelerometerData.shape[0]/100)
    accelerometerData = accelerometerData[:fullHoundreds*100].reshape(fullHoundreds, 100, 3)

    X = accelerometerData
    
    start = time.time()
    predictions = model.predict(X)
    end = time.time()
    time_needed = end - start

    y_pred = np.round(predictions).astype(int).reshape(1, -1)[0]

    suma = mean([float(i[0]) for i in predictions])
    numberofzeros = len([i for i in y_pred if i == 0])
    numberofones = len([i for i in y_pred if i == 1])

    if (numberofones > numberofzeros):
        result = 'driving'
        confidence = (1 - suma) * 100
    else:
        result = 'walking'
        confidence = suma * 100

    data = {
        "status": "success",
        "whichAlgorithm": "cnn",
        "accelerometerData": accelerometerData,
        "result": result,
        "confidence": confidence,
        "time_needed": time_needed,
        "numberofzeros": numberofzeros,
        "numberofones": numberofones
    }
    
    return jsonify(data)
