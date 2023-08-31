import yfinance as yf
import pandas as pd
import datetime as dt
import time
from datetime import timedelta
import pandas_ta as ta

from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

from functools import reduce
from sklearn.model_selection import GridSearchCV

#######################################################################################​
def get_data(ticker, year,month,day):
    start = dt.datetime(1999,1,1)
    end = dt.datetime.now()
     

    df = yf.download(ticker,start,end)
    return df

# loop through dataframe and add all features to a list
# removes 'Tomorrow' and 'Target' column from the list 
def get_features(dataframe):
    features = []
    for column in dataframe:
        features.append(column)
    
    features.pop(-1)
    features.pop(-1)
    
    return features

########################################################################################
# get raw data (2001 to now)
# pull SPY data
data = get_data('SPY',1999,1,1)
df = data.copy()
# pull oil data
oil_data = get_data('CL=F',1999,1,1)
oil_df = oil_data.copy()
# pull gold data 
gold_data = get_data('GC=F',1999,1,1)
gold_df = gold_data.copy()
#############################################################################################
# add and remove features
# SPY
df['Range'] = abs(df['High']-df['Low'])
df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'] )
df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'] )
df['Up'] = (df['Close'] > df['Open']).astype(int)
df['Percent Change'] = (abs(df['Close'] - df['Open']) / df['Open']) *100
df['MOM 5'] = ta.mom(df['Close'],5)
df['MOM 20'] = ta.mom(df['Close'],20)
df['RSI 14'] = ta.rsi(df['Close'], 14)
# remove adjusted close column
del df['Adj Close']

# Oil
oil_df['Oil Range'] = abs(oil_df['High']-oil_df['Low'])
oil_df['Oil ATR'] = ta.atr(oil_df['High'], oil_df['Low'], oil_df['Close'] )
oil_df['Oil Up'] = (oil_df['Close'] > oil_df['Open']).astype(int)
oil_df['Oil Percent Change'] = (abs(oil_df['Close'] - oil_df['Open']) / oil_df['Open']) *100
oil_df['Oil MOM 5'] = ta.mom(oil_df['Close'],5)
oil_df['Oil MOM 20'] = ta.mom(oil_df['Close'],20)
oil_df['Oil RSI 14'] = ta.rsi(oil_df['Close'], 14)
# remove price columns
del oil_df['Open']
del oil_df['Close']
del oil_df['High']
del oil_df['Low']
del oil_df['Volume']
del oil_df['Adj Close']
# Gold
gold_df['Gold Range'] = abs(gold_df['High']-gold_df['Low'])
gold_df['Gold ATR'] = ta.atr(gold_df['High'], gold_df['Low'], gold_df['Close'] )
gold_df['Gold Up'] = (gold_df['Close'] > gold_df['Open']).astype(int)
gold_df['Gold Percent Change'] = (abs(gold_df['Close'] - gold_df['Open']) / gold_df['Open']) *100
gold_df['Gold MOM 5'] = ta.mom(gold_df['Close'],5)
gold_df['Gold MOM 20'] = ta.mom(gold_df['Close'],20)
gold_df['Gold RSI 14'] = ta.rsi(gold_df['Close'], 14)
# remove price columns
del gold_df['Open']
del gold_df['Close']
del gold_df['High']
del gold_df['Low']
del gold_df['Volume']
del gold_df['Adj Close']
###################################################################################################
# merge dataframes
# merge SPY and oil dataframes
merged_oil = df.merge(oil_df, how='inner', on='Date')
# merge gold with already merged dataframe
merged_df = merged_oil.merge(gold_df, how='inner', on='Date')
#####################################################################################################
# create tomorrow and target columns
# it's the 'Close' value from the previous day
# will be used to create a target
merged_df['Tomorrow'] = merged_df['Close'].shift(-1)
merged_df['Target'] = (merged_df['Tomorrow'] > merged_df['Close']).astype(int)

## Create our candlestick df
candlestick_df = pd.DataFrame({
    'Open':merged_df['Open'],
    'High': merged_df['High'],
    'Low': merged_df['Low'],
    'Close': merged_df['Close'],
    'Volume': merged_df['Volume']
})

#del merged_df['High']
#del merged_df['Low']
#del merged_df['Open']
#del merged_df['Close']
del merged_df['Volume']

print(candlestick_df)
# save last row with NaN for tomorrow 
# will be used for daily predictions
most_recent = merged_df[-1:].copy()

# remove last row
merged_df.dropna(inplace=True)
merged_df


#####################################################################################################
# functions for backtesting
def predict(train, test, features, model):
    model.fit(train[features], train["Target"])
    preds = model.predict(test[features])
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

def backtest(df, model, features, start=2500, step=250):
    all_predictions = []
    backtest_data = []
    for i in range(start, df.shape[0]-step, step):
        train = df.iloc[0:i].copy()
        test = df.iloc[i:(i+step)].copy()
        predictions = predict(train, test, features, model)
        all_predictions.append(predictions)
        backtest_dict = {
        'start date':df.index[i-step],
        'end date': df.index[i],
        'precision score': precision_score(predictions["Target"], predictions["Predictions"]),
                }
        backtest_data.append(backtest_dict)
    backtest_df = pd.DataFrame(backtest_data)
    print(backtest_df)

    return backtest_df
    ## return pd.concat(all_predictions)

# perform backtest
# define model
n_estimators = 700
min_samples_split = 400
max_depth = 4

model = RandomForestClassifier(n_estimators=n_estimators, min_samples_split=min_samples_split, max_depth=max_depth, random_state=1)
# run back test for previous periods
backtest_predictions = backtest(merged_df, model, get_features(merged_df))
    # returns dataframe with time period column and precision column
print(backtest_predictions)


#######################################################################################################
# function for making daily prediction
def daily_prediction(df,model,most_recent): 
    features = get_features(df)
    train = df.iloc[:-1000]
    test = df.iloc[-1000:]
    model.fit(train[features], train['Target'])
    prediction = model.predict(most_recent[features])
    print(prediction)
    return prediction

todays_prediction = daily_prediction(merged_df,model,most_recent)

    # return 1 for buy signal, 0 for don't buy signal

print(todays_prediction[0])

################################################################################################

# same as fit_train_score but it excepts arguments for max_depth
def fit_train_score_with_depth(df, n_est, min_split, max_depth):
    features = get_features(df)
    # n_estimators = number of decision trees
    # min_samples_split = higher it is set, the less accurtate it is, the less it will overfit
    model = RandomForestClassifier(n_estimators=n_est, min_samples_split=min_split, random_state=1)
    train = df.iloc[:-1000]
    test = df.iloc[-1000:]
    # fit and train model
    model.fit(train[features], train['Target'])
    predictions = model.predict(test[features])
    #predictions_series = pd.Series(predictions, index=test.index)
    # precision of training data
    predictions_training = model.predict(train[features])
    test_dict = {
        'n_estimators':n_est,
        'min_samples_split':min_split,
        'max_depth': max_depth,
        'training precision':precision_score(train['Target'], predictions_training),
        'testing precision':precision_score(test['Target'], predictions)
                }
    return test_dict



test_dict = fit_train_score_with_depth(merged_df, n_estimators, min_samples_split, max_depth)

## Write backtest_df, merged_df to csv

## Where do we store sample size and precision scores


###### These have already run, commenting out so they don't break the code
###  backtest_predictions.to_csv('results/backtest_data.csv')
# merged_df.to_csv('results/merged_data.csv')
candlestick_df.to_csv('results/candlestick_data.csv')
final_day = most_recent.index



print(final_day)
print(most_recent)
print("Model Ready to Load")
