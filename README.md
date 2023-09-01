# project-four
Repo for Project 4 WUSTL Data Class


# Stock Prediction w/ Random Forest Machine Learning Model
For this project, our group developed a Random Forest machine learning model to predict intraday price action for the S&P 500 index. 


## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Installing](#installing)
- [Usage](#usage)
- [Contributing](#contributing)

## About
The model is trained on data from SPY, an ETF that tracks the S&P 500. The model then predicts whether the price of SPY will increase or decrease over the course of the next trading day.
An increase occurs when the closing price on the current day is greater than the closing price of the previous day. A decrease occurs then the closing price on the current day is less than the closing price of the previous day. From this, a recommendation is created whether the user should buy or not buy. Backtesting was also used to determine the precision of model over varying time periods. The model, recommendation, back testing, and historical price data are displayed on webpages. The index html displays information regarding the model and a recomendation for the user to buy or not buy. The candlestick webpage shows the accuracy scores from the backtesting along w/ a candlestick chart for a year chosen by the user. 

## Getting Started
4. Run the Flask.py app.
5. Run the either the candlestick html or the index html. 


## Installing
1. Downloading yahoo finance API - see https://pypi.org/project/yfinance/ for instructions

## Usage
1. Load either candlestick HTML or index HTML.
2. Switch between the candlestick HTML and index HTML by using the link on the webpage. 
3. On the candlestick HTML, use the drop down to select a year to display the candlestick chart for that year. 

## Contributing
Kenny Siegler, Ed Shanks, Hannah Weber

## Resources
Yahoo Finance API - https://pypi.org/project/yfinance/ 
Plotly Demo Candlestick - https://plotly.com/python/candlestick-charts/ 
