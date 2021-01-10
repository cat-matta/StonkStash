import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats



raw_data = pd.read_csv("sp500.csv")

raw_data.head()
stdstuff = raw_data['High'].std()
meanstuff = raw_data['High'].mean()

print(stdstuff,meanstuff)