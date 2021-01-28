import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style ##wanna make graphs look aesthetic as you lose money
import pandas_datareader.data as web ##get our data from yahoo
import pandas as pd##we use pandas
style.use('ggplot')##style of graph

start = dt.date(2021,1,1)##start date
end = dt.date(2021,1,26)##end data

dataframe = web.DataReader('GME','yahoo',start,end) ## we get this data from yahoos public api
##dataframe.head()##Show some of the data
dataframe.to_csv('gamestopmeme.csv') ##converts our data to a csv

df = pd.read_csv('gamestopmeme.csv', parse_dates=True,index_col=0) ##DataFrame


df["High"].plot()##plots highs
df["Low"].plot()##plots lows
plt.show()##shows the plot