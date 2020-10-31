# This program is used to split the data set into train_X, train_y, test_X, test_y

# Imports
import pandas as pd
import json
from pandas.io.json import json_normalize

# Reads the raw data and deletes unwanted symbols
df = pd.read_csv('out.csv')
del df['After']
del df['Before']
del df['symbol']

# Separates data into train and test sets
train=df.sample(frac=0.8)
test=df.drop(train.index)

# Separates data into X and y sets
train_y = train['PercentIncrease']
del train['PercentIncrease']
train_X = train

test_y = test['PercentIncrease']
del test['PercentIncrease']
test_X = test

# Exports data
train_y.to_csv('train_y.csv', mode='w', header=True, index=False)
train_X.to_csv('train_X.csv', mode='w', header=True, index=True)
test_y.to_csv('test_y.csv', mode='w', header=True, index=False)
test_X.to_csv('test_X.csv', mode='w', header=True, index=False)