import hello
import main
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
print("Hello World")


'''
Alright so Read this before reading my code.


This is actually more complicated than i thought it was.

so we have three changes going on.


for us to calculate risk 2.0

we need to calculate 2 things for now.


Volume 
Movement


These two movements have rate of changes as its good to know the rate of change for both variables


Volume = Share's bought or sold.
Movement = Stock price going up or down.


If a stocks movement within 7 days has drastically changed. Stock is high risk

if the shares bought or sold are drastically changing within 3 days. Many people buying or selling.




'''


periods= {"w": "week", "m": "month", "q": "quarter", "s": "semianual", "y": "year"} # We are gonna need periods for this

getStockPrice('AMZN')