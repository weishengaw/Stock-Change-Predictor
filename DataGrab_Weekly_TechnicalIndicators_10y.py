# This program is used to grab stock price and technical indicator data of the S&P 500
# This program might take several hours to run, depending on how far back you want to go and the frequency of the data

# Quick Variable Changes

# Counter for update purposes
# 1 if you want to add data to dataset, 0 if you want to create new dataset
count = 0

# Initialize beginning and end times of data grab in unix
f = 1284816600
t = 1600435800

# Resolution: how frequent data is collected (D, W, M)
r = 'W'

# Offset: how far between stock price and features do you want in seconds
tb = 604800

# imported packages
import pandas as pd
import finnhub
import json
from pandas.io.json import json_normalize
import time

# Gets the symbols of every item in the S&P 500
# Note: Some stocks with barely any financial data will most likely fail, I put code to catch it but it is not foolproof
#       E.g. OTIS
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
sp_symbols = df['Symbol']

# You can modify 'sp500.txt' to collect data from any set of companies you want
# Comment out the above list if you do so
# df3 = pd.read_csv('sp500.txt', sep=";", names=['Tickers'])
# sp_symbols = df3['Tickers']

# Gets the finnhub client to use the api
finnhub_client = finnhub.Client(api_key="bt4an7v48v6ue5eg9c6g")

# Loops through each ticker in the sp500, or each ticker wanted
for index, value in sp_symbols.items():
    # The flag/while/try/except structure makes sure the program does not overload the API
    flag = True
    while flag:
        try:
            # res calls the stock candle history for the given ticker, time frame, and frequency
            res = finnhub_client.stock_candles(symbol=value, resolution=r, _from=f, to=t)
            res2 = finnhub_client.stock_candles(symbol=value, resolution=r, _from=f-tb, to=t-tb)
            flag = False
        except:
            time.sleep(.1)

    # Converts candles to dataframe and singles out closing prices
    try:
        tempPricesA = pd.DataFrame(res)
        tempPricesB = pd.DataFrame(res2)
        y = pd.concat([tempPricesA['c'], tempPricesB['c']], axis=1)
        num = y.shape[0]
        temp = pd.Series(value, index=range(0, num))

        # Calculates Percent Increase of each data point
        y = pd.concat([y, temp], axis = 1)
        symbols = ['After', 'Before', 'symbol']
        y.columns = symbols
        y['PercentIncrease'] = (y['After'] - y['Before']) / y['Before']
        print(value + ' y data grabbed!')

        
        # Grabs list of supported technical indicators 
        df2 = pd.read_csv('Indicators.txt', sep=";", names=['Indicators'])
        ind_symbols = df2['Indicators']

        # Initializes X (feature) matrix
        X = pd.DataFrame()
        X = pd.concat([X, y], axis=1)
        
        flag2 = True
        # Loops through each technical indicators
        for index2, value2 in ind_symbols.items():

            count2 = 0
            # Similar structure as above to get technical indicators
            flag = True
            while flag and count2 < 30:
                try:
                    res2 = finnhub_client.technical_indicator(symbol=value, resolution=r,
                            _from= f-tb, to=t-tb, indicator=value2,
                            indicator_fields={"timeperiod": 3, "seriestype": None})
                    flag = False
                except:
                    time.sleep(.1)
                    count2 += 1
            if count2 >= 30:
                flag2 = False
            
            # Converts technical indicator data into dataframe
            tempIndicators = pd.DataFrame(res2)

            # Deletes unwanted information from indicators
            del tempIndicators['c']
            del tempIndicators['h']
            del tempIndicators['l']
            del tempIndicators['o']
            del tempIndicators['s']
            del tempIndicators['t']
            del tempIndicators['v']

            # Adds information to the feature matrix
            try:
                X = pd.concat([X, tempIndicators], axis=1)
            except:
                print(value + ' Skipped')
                flag2 = False
        
        # Removes 0s, or values that are not found
        X = X[(X.T != 0).all()]
        X.dropna(axis=0)

        # Adds collected data from X and y and exports it to the csv file
        if (count == 0):
            X.to_csv('out.csv', mode='w', header=True, index=False)
        else:
            X.to_csv('out.csv', mode='a', header=False,index=False)     
        count += 1
        print(value + ' X data grabbed')
    except:
        continue
    
