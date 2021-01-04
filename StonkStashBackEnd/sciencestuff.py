import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# initialization and filtering the data

df = pd.read_csv('all_stocks_5yr.csv') # reading the csv file into our data frame
periods= {"w": "week", "m": "month", "q": "quarter", "s": "semianual", "y": "year"} # different periods for the graphs to be shown in

# print(df.head()) # checking the first 5 rows
# print(df.dtypes) # checking the type of data we are working with here
# print(df.isnull().sum()) # this tells us which values are null

# we dont really care for the opening and closing since those are unpredicatable
df = df.dropna(axis = 0, subset = ['high','low']) # cleaning up the rows that contain NaN for the high and the low
# print(df.isnull().sum()) # now we can see if we cleaned it up right

def get_user_input(): # what stock and date does the user want to look at?
    # later on, one can implement a change date/stock feature
    print("Input a stock name and a specific date")
    stock_name, stock_date = input("format: NAME, yr-mon-day: ").split(", ") # getting the two parameters
    return stock_name, stock_date

stock_name, stock_date=get_user_input() # getting the data
want = df.loc[(df['Name'] == stock_name) & (df['date'] == stock_date)] # getting the values that the user wanted
want_high = want.high # getting the high value
want_low = want.low
date = df.index[0] # getting the date index 
print("High: {}\nLow: {}\n".format(want_high,want_low)) # just for debugging

def filter_data(dataframe,stock_name,date,period): # we can add options for the period later
    filtered_name = dataframe.loc[dataframe['Name']==stock_name] # filtering based on the name of the stock that was given
    filter_all=filtered_name.filter(items=['date','high','low']) # filtering the stuff
    # if you want more data, add the column name in the list
    # the conditional stuff is just for the periods that are in the dictionary
    if(period== 'm'):
        start_date = date - 29
        period=periods.get(period)
    elif(period == 'w'):
        start_date = date - 6
        period=periods.get(period)
    elif(period == 's'):
        start_date = date - 181
        period=periods.get(period)
    elif(period == 'q'):
        start_date= date - 89        
        period=periods.get(period)
    elif(period == 'y'):
        start_date = date - 364
        period=periods.get(period) 
    end_date = date + 1 # adding 1 for the indexing
    graph_stuff(filtered_name,start_date,end_date,period) # now we graph

def graph_stuff(dataframe,start_date,end_date,period):
    fig = plt.figure(figsize=(10,5)) # size of the figure
    sns.lineplot(data=dataframe[start_date:end_date:],x='date',y='high',label='High',color='g') # for the highs
    sns.lineplot(data=dataframe[start_date:end_date:],x='date',y='low',label='Low',color='r') # for the lows
    # plt.xticks(rotation='vertical') # looks horrid
    # i need to add some type of increments
    string="{} Stock Data for the {} ending {}".format(stock_name, period,stock_date) # for the title
    plt.title(string)
    plt.ylabel('Price [$]') # y axis
    plt.xlabel('Date [yr-mon-day]') # x axis
    save = "plots/{}_{}_{}.png".format(stock_name,stock_date,period) # to save the output and give it a name
    fig.savefig(save) # saving the figure
    plt.show() # displaying it

filter_data(df, stock_name, date,'y')



