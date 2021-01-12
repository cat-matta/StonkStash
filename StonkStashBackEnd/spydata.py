import pandas as pd 

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns## this library relies on the libraries above so please import everything


raw_data = pd.read_csv("sp500.csv")## Reads the csv file

raw_data.head()##Getting first 5 values
stdstuff = raw_data['High'].std()##finds the standard deviation for high
meanstuff = raw_data['High'].mean()##finds the mean

print(stdstuff,meanstuff) ## I think you should know already what this does -_-