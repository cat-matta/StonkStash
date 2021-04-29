import urllib.request
from bs4 import BeautifulSoup
import json
from datetime import datetime

####FUNCTION SIGNATURES###############################################
#                                                                   ##
# getSimpleMovingAverage(values, days)                              ##
# getEMA(values, days)                                              ##
# getMACD(closes)                                                   ##
# getSoup(stockSymbol, startUnixTime, endUnixTime, interval)        ##
# soupToStockPrices(soup)                                           ##
# getStockPrices(stockSymbol, startUnixTime, endUnixTime, interval) ##
#                                                                   ##
######################################################################

#param: values is a list of floats
#       we will be calculating the simple moving average of the first
#       n elements of values, where n is days
#       days is an int with the number of days in the period
#
#return: float with the simple moving average of the first n values, where n is days
#        simple moving average is just the average
#
#Note: this is a helper function called by getEMA, which is also a helper function
def getSimpleMovingAverage(values, days):

    sumOfFirstDaysValues = sum(values[:days])
    simpleMovingAverage = sumOfFirstDaysValues/days

    return simpleMovingAverage


#param: values is a list of strings containing numbers or floats
#       we will be calculating as many EMA values of this list as we can
#       days is an int with the number of days in the period
#
#return: list with EMA values
#
#Note: this is a helper function called by getMACD and getStockPrices,
#      the former of which is also a helper function
def getEMA(values, days):

    #the initial EMA value can be taken to be the simple moving average (SMA)
    #(EMA is defined recursively, so we need a base case. That base case is the SMA)
    exponentialMovingAverage = getSimpleMovingAverage(values, days)

    #this multiplier is a part of the formula
    multiplier = 2/(1+days)

    #this loop computes all of the EMA values we will return
    numberOfValues = len(values)
    EMA = []
    for value in values[days: numberOfValues]:
        exponentialMovingAverage = value*multiplier + exponentialMovingAverage*(1-multiplier)
        EMA.append(exponentialMovingAverage)

    return EMA


#param: closes is a list of floats containing all of the close prices
#
#return: list of MACD values
#
#Note: this is a helper function called by getStockPrices
def getMACD(closes):

    #twelveDayEMA and twentySixDayEMA are lists with the 12 and 26 day EMA's respectively
    twelveDayEMA = getEMA(closes, 12)
    twentySixDayEMA = getEMA(closes, 26)

    numberOfMACDvaluesWeCanCompute = len(twentySixDayEMA)

    #MACD is 12 day EMA - 26 day EMA
    MACD = [twelveDayEMA[-i-1] - twentySixDayEMA[-i-1] for i in range(numberOfMACDvaluesWeCanCompute)]

    return MACD


#param: stockSymbol is a string containing the symbol of the stock we're interested in
#       startUnixTime is the unix timestamp of the date of the oldest stock price we're looking for
#       endUnixTime is the unix timestamp of the date of the most recent stock price we're looking for
#       interval is a string, one of H, D, W, M, which indicates how spaced apart the stock prices should be
#
#return: soup of the html of the page containing the stock prices indicated by the parameters
#
#Note: this is a helper function called by getStockPrices
def getSoup(stockSymbol, startUnixTime, endUnixTime, interval):

    intervals = {'H': '1h', 'D': '1d', 'W': '1wk', 'M': '1mo'}

    #generate url from the above parameters
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stockSymbol}?symbol={stockSymbol}&period1={startUnixTime}&period2={endUnixTime}&useYfid=true&interval={intervals[interval]}&includePrePost=true&lang=en-US&region=US&crumb=MuMxQThgteG&corsDomain=finance.yahoo.com"

    #soupify the html from the above url
    opener = urllib.request.urlopen(url)
    stonksoup = BeautifulSoup(opener, 'lxml')

    return stonksoup


#param: soup is a BeautifulSoup object of the page with the stock prices we're interested in
#       the other parameters are lists of strings containing what their name suggests
#
#return: list of six lists containing, in order: unix timestamps, open, high, low, close prices, 
#        and volume traded
#
#Note: this is a helper function called by getStockPrices
def soupToStockPrices(soup):

    #all of the information in the page is in a p tag, the contents of the p tag are in json format
    info = json.loads(soup.find('p').text)["chart"]["result"][0]

    stockPrices = info["indicators"]["quote"][0]
    return [info["timestamp"]] + [stockPrices[key] for key in ["open", "high", "low", "close", "volume"]]


#valid data granularities in yahoo finance: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

#param: stockSymbol is a string with the symbol of the stock we're interested in      
#       startUnixTime and endUnixTime are ints or floats containing unix timestamps of the
#        oldest and most recent stock prices we're interested in, respectively
#       interval is a string indicating how spaced out the stock prices are where it can be one of
#        H, D, W, M standing for hourly, daily, weekly, and monthly respectively
#
#return: dict with the open, low, high, close prices, volume traded, and MACD values
#         for the stock in stockSymbol from the period enclosed by startUnixTime and endUnixTime
def getStockPrices(stockSymbol, startUnixTime, endUnixTime, interval):

    #first we get the stock prices we're interested in, then we get 
    #more stock prices to accurately compute MACD values
    
    #get stock prices and volume traded over period we're interested in
    stonksoup = getSoup(stockSymbol, startUnixTime, endUnixTime, interval)

    #list with six lists, in order: timestamps, open, high, low, close prices, volume traded
    stonks = soupToStockPrices(stonksoup)

    #number of stock prices we obtained above. 
    #we could have taken the length of any of the lists in stonks
    numberOfPrices = len(stonks[0])

    #get more stock prices, these will be used to more accurately compute MACD values
    extraUnixTime = {'H': 2_808_000, 'D': 31_449_600, 'W': 157_248_000, 'M': 336_960_000}
    stonksoup = getSoup(stockSymbol, startUnixTime-extraUnixTime[interval], startUnixTime, interval)
    extraStonks = soupToStockPrices(stonksoup)

    #combine the stock prices we're interested in and the extra stock prices in a single list
    stonks = [extraStonk + stonk for (stonk, extraStonk) in zip(stonks, extraStonks)]
    
    MACD = getMACD(stonks[4]) #stonks[4] is the list with the close prices

    #we reverse MACD because getEMA expects a list with the oldest value at index 0
    #we reverse the return value so that the list has the most recent value at index 0
    signalLine = getEMA(MACD[::-1], 9)[::-1] #signal line is 9 day EMA of MACD

    macdHistogram = [MACD[i] - signalLine[i] for i in range(numberOfPrices)] #histogram is macd - signal line

    #this preserves only the values obtained in the first call to soupToStockPrices
    stonks = [valuesList[:-numberOfPrices-1:-1] for valuesList in stonks]

    #convert unix timestamps to strings with the date and time
    stonks[0] = [datetime.utcfromtimestamp(timestamp).strftime('%m-%d-%Y %H:%M:%S') for timestamp in stonks[0]]

    return dict(zip(["date", "open", "high", "low", "close", "volume", "MACD", "MACD-Signal", "MACD-Hist"], stonks + [MACD[:numberOfPrices], signalLine[:numberOfPrices], macdHistogram]))
