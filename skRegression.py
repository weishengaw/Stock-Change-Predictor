# Basic Linear Regression function for the stock indicator dataset
# Uses scikit-learn package, and uses pickle to store the model

# Imports
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
import pandas as pd
import pickle

# Loads data sets
train_X = pd.read_csv('train_X.csv')
test_X = pd.read_csv('test_X.csv')
train_y = pd.read_csv('train_y.csv')
test_y = pd.read_csv('test_y.csv')

# Converts data into numpy arrays
a1 = train_X.to_numpy()
a2 = train_y.to_numpy()
a3 = test_X.to_numpy()
a4 = test_y.to_numpy()

# Scales test and train X
scaler = preprocessing.StandardScaler().fit(a1)
scaler.mean_
scaler.scale_
scaler.transform(a1)
scaler.transform(a3)

# Fits model
regr = linear_model.LinearRegression()
regr.fit(a1, a2)

# Predicts using test set and displays metrics
pred = regr.predict(a3)
print(mean_squared_error(a4, pred))
print(r2_score(a4, pred))

# Saves model
model_path = r"model.pickle"
pickle.dump(regr, open(model_path, 'wb'))