from pydoc import doc
from flask import Flask, jsonify
import json
from flask_cors import CORS

from model import *

app = Flask(__name__)
CORS(app)


@app.route("/api/results")
def display_result():
    ## Create a dictionary with hardcoded values here and deploy them to JS?
    data_dict = {
        "Sample Size": 10000,
        "Model Type": "Randomized Tree",
        "Model Size": "500 Layers",
        "Training Precision": .6148,
        "Testing Precision": .6111,
        "Prediction": 1

    }
    return data_dict
    

@app.route('/api/backtest')
def backTest():

    return "This is where we run our backtesting"



if __name__ == "__main__":
    app.run(debug=True)