##import sciencestuff as coolbeans
import numpy as np ## feel free to comment this out
import time
import main

'''okay so to calculate the volitility i need you to use these functions with the csv file. I will also provide a definition.

Volitiy is basically how risky a stock is, does it have huge risk? or low risk? thats what volitily will tell us. Below will be a function to help us find volitilty.

Here's a link just in case
https://www.investopedia.com/terms/v/volatility.asp
if you have any questions let me know
DO NOT I REPEAT , DO NOT GO ON WALL ST BETS I SWEAR TO GOD

'''

def riskyboi(arr): ##it will take a list as a input
    riskystocks = np.array(arr);## we basically created a numpy array with np.array
    riskyboicalc = np.std(riskystocks); ## Standard deviation for the array
    '''for this, it should be a simple calculation. All we need is the standard deviation. Also we're gonna be a little conserviative for risk factor. 
    if the std deviation is above 0.5 thats high risk
    else if its lower than 0.5 its low risk '''
    if(riskyboicalc >= 0.5):
        return "This stock is high risk";
    else:
        return "This stock is low risk";

def sharesbought(arr): ##how many shares bought
    volume = np.array(arr);##this will come from the volume dataset
    bought = np.mean(volume);##since its an array we need the average for time period
    return bought;
    
def getHighAndLow(companyName):
    stock_candles = main.getStockCandlesToday(companyName)
    high = stock_candles['h']
    low = stock_candles['l']
    highChange = []
    lowChange = []
    highAndLowDiff = []
    for i in range(len(high)-1):
        highChange.append(high[i+1]-high[i])
        lowChange.append(low[i+1]-low[i])
        highAndLowDiff.append((high[i]-low[i])*100/high[i])
    
    return highChange,lowChange,highAndLowDiff;

def driver():
    #put in the desired company's stock symbol
    stock_name = "AMZN"
    
    highChange, lowChange, highAndLowDiff = getHighAndLow(stock_name)
    
    #volatility of the high prices
    print(riskyboi(highChange))
    
    #volatility of the low prices
    print(riskyboi(lowChange))
    
    #this computation might not be meaningful, but it gives an idea of
    #how widely the stock ranges each day as a percentage of its current high
    print(highAndLowDiff)

driver()
