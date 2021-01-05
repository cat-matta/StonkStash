import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import main

periods= {"w": "week", "m": "month", "q": "quarter", "s": "semianual", "y": "year"} # different periods for the graphs to be shown in

def get_user_input(): # what stock and date does the user want to look at?
    # later on, one can implement a change date/stock feature
    print("Input a stock name and a specific date")
    stock_name, stock_date = input("format: NAME, yr-mon-day: ").split(", ") # getting the two parameters
    return stock_name, stock_date
    
def graph_stuff(dataframe,name,date,period):
    fig = plt.figure(figsize=(10,5)) # size of the figure
    sns.lineplot(data=dataframe['h'], label='High', color='g') # for the highs
    sns.lineplot(data=dataframe['l'], label='Low',color='r') # for the lows
    # plt.xticks(rotation='vertical') # looks horrid
    # i need to add some type of increments
    string="{} Stock Data for the {} ending {}".format(name,periods[period],date) # for the title
    plt.title(string)
    plt.ylabel('Price [$]') # y axis
    plt.xlabel('Date [yr-mon-day]') # x axis
    save = "plots/{}_{}_{}.png".format(name,date,period) # to save the output and give it a name
    fig.savefig(save) # saving the figure
    plt.show() # displaying it
    
def driver():
    resolution = 'D' #resolution can be any one of 1, 5, 15, 30, 60, D, W, M
    period = 'y' #period can be any one of w, m, q, s, y
    
    stock_name, stock_date=get_user_input() #asks user for a stock name and date
    desiredData = main.getStockCandles(stock_name,resolution,stock_date,period) #getting data
    graph_stuff(desiredData,stock_name,stock_date,period) # now we graph
    
driver()
