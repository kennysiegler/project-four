from pydoc import doc
from flask import Flask, jsonify
import json
from flask_cors import CORS
import csv

from model import *

app = Flask(__name__)
CORS(app)



def createCandlestickDictionary():
    # l should be passed as a list, it will be equivalent to the row
    candlesticks = {}
    for i in range(2000,2024):
        candlesticks[str(i)] = {"dates": [], "open": [], "high": [], "low": [], "close": [], "volume": []}    
    return candlesticks
        
@app.route("/api/results")
def display_result():
    ## Create a dictionary with hardcoded values here and deploy them to JS?
    data_dict = {
        "Training Sample Size": len(merged_df),
        "Model Type": "Random Forest Model",
        "Model Size": f"{n_estimators} Layers",
        "Training Precision": test_dict['training precision'],
        "Testing Precision": test_dict['testing precision'],
        "Prediction": int(todays_prediction[0])

    }
    return data_dict
    

@app.route('/api/backtest')
def backTest():

    with open('results/backtest_data.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar="|")
        next(reader)

        total_dict = {}

        for row in reader:
            start_date = row[1]
            end_date = row[2]
            precision_score = row[3]
            
            total_dict[f'{start_date} - {end_date}'] = round(float(precision_score),4)*100
            
            
    return total_dict

@app.route('/api/candlestick')
def displayCandlestick():
    ## clearCandleSticks()
    candlesticks = createCandlestickDictionary()
    with open('results/candlestick_data.csv') as file:
        candlestick_reader = csv.reader(file, delimiter=',', quotechar='|')
        next(candlestick_reader)
        for row in candlestick_reader:
           for i in range(2000,2024):
                if row[0][:4] == str(i):
                
                    candlesticks[str(i)]['dates'].append(row[0])
                    candlesticks[str(i)]['open'].append(row[1])
                    candlesticks[str(i)]['high'].append(row[2])
                    candlesticks[str(i)]['low'].append(row[3])
                    candlesticks[str(i)]['close'].append(row[4])
                    candlesticks[str(i)]['volume'].append(row[5])
        print(candlesticks)
        return candlesticks
    
    


if __name__ == "__main__":
    app.run(debug=True)