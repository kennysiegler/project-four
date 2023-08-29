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


def get_data(ticker, year,month,day):
    start = dt.datetime(1999,1,1)
    end = dt.datetime.now()
     

    df = yf.download(ticker,start,end)

    return df
df = get_data('SPY', 1999,1,1)

# loop through dataframe and add all features to a list
# removes 'Tomorrow' and 'Target' column from the list 
def get_features(dataframe):
    features = []
    for column in dataframe:
        features.append(column)
    
    features.pop(-1)
    features.pop(-1)
    
    return features

    # create new features
df['Range'] = abs(df['High']-df['Low'])
df['RSI 14'] = ta.rsi(df['Close'], 14)
df['SMA 20'] = ta.sma(df['Close'], 20)
df['SMA 50'] = ta.sma(df['Close'], 50)
df['SMA 200'] = ta.sma(df['Close'], 200)
df['EMA 12'] = ta.ema(df['Close'], 12)
df['EMA 26'] = ta.ema(df['Close'], 26)
df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'] )

# create 'Tomorrow' column
# it's the 'Close' value from the previous day
# will be used to create a target
df['Tomorrow'] = df['Close'].shift(-1)
df['Target'] = (df['Tomorrow'] > df['Close']).astype(int)
df = df.copy().loc['2000-01-01':]
df.drop('Adj Close', axis=1, inplace=True)
df.drop(df.tail(1).index, inplace=True)

# get foreign market and gold data
UK_df = get_data('^FTSE',1999,1,1)
China_df = get_data('000001.SS',1999,1,1)
Germany_df = get_data('^GDAXI',1999,1,1)
Japan_df = get_data('^N225',1999,1,1)
gold_df = get_data('GC=F',1999,1,1)


# clean foreign market data
# some have empty volume columns for early 2000's

# drop volume from foreign data dfs
#rename columns
# remove first year of dat

UK_df.drop(['Volume', 'Adj Close'], axis=1, inplace=True)
UK_df.rename(columns={
    'Open':'UK Open',
    'High':'UK High',
    'Low':'UK Low',
    'Close':'UK Close'
},inplace=True)
UK_df.loc['2000-01-01':]

China_df.drop(['Volume', 'Adj Close'], axis=1, inplace=True)
China_df.rename(columns={
    'Open':'China Open',
    'High':'China High',
    'Low':'China Low',
    'Close':'China Close'
},inplace=True)
China_df.loc['2000-01-01':]

Germany_df.drop(['Volume', 'Adj Close'], axis=1, inplace=True)
Germany_df.rename(columns={
    'Open':'Germany Open',
    'High':'Germany High',
    'Low':'Germany Low',
    'Close':'Germany Close'
},inplace=True)
Germany_df.loc['2000-01-01':]

Japan_df.drop(['Volume', 'Adj Close'], axis=1, inplace=True)
Japan_df.rename(columns={
    'Open':'Japan Open',
    'High':'Japan High',
    'Low':'Japan Low',
    'Close':'Japan Close'
},inplace=True)
Japan_df.loc['2000-01-01':]

gold_df.drop(['Volume', 'Adj Close'], axis=1, inplace=True)
gold_df.rename(columns={
    'Open':'Gold Open',
    'High':'Gold High',
    'Low':'Gold Low',
    'Close':'Gold Close'
},inplace=True)
gold_df.loc['2000-01-01':]

# merge into one df
dfs = [UK_df, China_df, Germany_df, Japan_df, gold_df, df]
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                            how='inner'), dfs)
test_dict = {
    "n": 5,
    "Accuracy": 0.61

}


