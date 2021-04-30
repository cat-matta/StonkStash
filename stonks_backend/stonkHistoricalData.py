import urllib.request
from bs4 import BeautifulSoup
import json
from datetime import datetime

####FUNCTION SIGNATURES################################################
#                                                                    ##
# eliminateNullValues(stonks)                                        ##
# getSimpleMovingAverage(values, days)                               ##
# getEMA(values, days)                                               ##
# getMACD(closes)                                                    ##
# getSoup(stockSymbol, startUnixTime, endUnixTime, interval)         ##
# soupToStockPrices(soup)                                            ##
# getRawExtraStockData(stockSymbol, startUnixTime, interval)         ##
# getRawStockData(stockSymbol, startUnixTime, endUnixTime, interval) ##
# cleanAndCombine(stonks, extraStonks)                               ##
# getStockPrices(stockSymbol, startUnixTime, endUnixTime, interval)  ##
#                                                                    ##
#######################################################################


#param: stonks is a list of lists, each list has the same number of values
#
#Note: this is a helper function called by cleanAndCombine,
#          which is a helper function called by getStockPrices
#      if an element in a list of stonks at index i is None, then the element at
#          index i of every list of stonks is deleted
def eliminateNullValues(stonks):

    #get list of indices to be deleted
    indicesWithNone = []
    for i in range(len(stonks[0])):
        currValues = [stonk[i] for stonk in stonks]
        if None in currValues:
            indicesWithNone.append(i)

    #after deleting one element, every subsequent element's index is decreased by 1
    #so the following line takes care of that
    indicesWithNone = [element-i for i, element in enumerate(indicesWithNone)]

    #deletes elements with None
    for stonk in stonks:
        for index in indicesWithNone:
            del stonk[index]


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
#Note: this is a helper function called by getMACD and cleanAndCombine,
#          both of which are helper functions called by getStockPrices
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
#Note: this is a helper function called by cleanAndCombine,
#          which is a helper function called by getStockPrices
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
#Note: this is a helper function called by getRawExtraStockData, 
#          which is a helper function called by getStockPrices
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
#Note: this is a helper function called by getRawStockData and getRawExtraStockData,
#          which are both helper functions called by getStockPrices
def soupToStockPrices(soup):

    #all of the information in the page is in a p tag, the contents of the p tag are in json format
    info = json.loads(soup.find('p').text)["chart"]["result"][0]

    stockPrices = info["indicators"]["quote"][0]
    return [info["timestamp"]] + [stockPrices[key] for key in ["open", "high", "low", "close", "volume"]]


#param: stockSymbol is a string with the symbol of the stock we're interested in      
#       startUnixTime is an int containing unix timestamp of the
#           oldest stock price we're interested in
#       interval is a string indicating how spaced out the stock prices are where it can be one of
#           H, D, W, M standing for hourly, daily, weekly, and monthly respectively
#
#return: list of six lists containing unix timestamps, open, high, low, close prices,
#           and volume of stocks traded over some period ending at the oldest stock price
#           requested. This gets additional data to compute macd values more accurately
#
#Note: this is a helper function called by getStockPrices
def getRawExtraStockData(stockSymbol, startUnixTime, interval):

    #how much extra data we get depends on the interval between consecutive stock prices
    extraUnixTime = {'H': 2_808_000, 'D': 31_449_600, 'W': 157_248_000, 'M': 336_960_000}
    stonksoup = getSoup(stockSymbol, startUnixTime-extraUnixTime[interval], startUnixTime, interval)
    return soupToStockPrices(stonksoup)


#param: stockSymbol is a string with the symbol of the stock we're interested in      
#       startUnixTime and endUnixTime are ints containing unix timestamps of the
#           oldest and most recent stock prices we're interested in, respectively
#       interval is a string indicating how spaced out the stock prices are where it can be one of
#           H, D, W, M standing for hourly, daily, weekly, and monthly respectively
#
#return: list of six lists containing timestamps, open, high, low, close prices, and
#           volume of stocks traded over the period specified by the parameters
#
#Note: this is a helper function called by getStockPrices
def getRawStockData(stockSymbol, startUnixTime, endUnixTime, interval):

    span = endUnixTime - startUnixTime

    #the body of this loop gets the page with stock info contains any data,
    #and breaks out of loop if data is obtained. If data isn't obtained in
    #5 tries, it just proceeds so as not to run forever. This could happen
    #if this function is called with a ticker that doesn't exist
    for _ in range(5):

        #generate url from the above parameters
        stonksoup = getSoup(stockSymbol, startUnixTime, endUnixTime, interval)

        info = json.loads(stonksoup.find('p').text)["chart"]["result"][0]
        stockPrices = info["indicators"]["quote"][0]

        #if it's not an empty dict, then break because we obtained data
        if stockPrices:
            break

        #if it is an empty dict, look for stock prices on a previous period of time
        endUnixTime = startUnixTime
        startUnixTime = startUnixTime - span

    if stockPrices:
        stonks = [info["timestamp"]] + [stockPrices[key] for key in ["open", "high", "low", "close", "volume"]]
    else:
        stonks = []

    return stonks, startUnixTime


#param: stonks and extraStonks are lists of six lists containing unix timestamps,
#           open, high, low, close prices, and volume of stocks traded over different
#           periods of time. stonks contains the data requested by the parameters in
#           getStockPrices, whereas extraStonks is extra data to compute macd values more
#           accurately.
#
#return: dictionary with all of the data requested by the parameters in getStockPrices
#
#Note: this is a helper function called by getStockPrices
def cleanAndCombine(stonks, extraStonks):

    #number of stock prices we obtained above requested by paramters in getStockPrices
    numberOfPrices = len(stonks[0])

    #combine the stock prices we're interested in and the extra stock prices in a single list
    stonks = [extraStonk + stonk for (stonk, extraStonk) in zip(stonks, extraStonks)]
    
    eliminateNullValues(stonks) #takes away all nulls in our data
    
    MACD = getMACD(stonks[4]) #stonks[4] is the list with the close prices

    #we reverse MACD because getEMA expects a list with the oldest value at index 0
    #we reverse the return value so that the list has the most recent value at index 0
    signalLine = getEMA(MACD[::-1], 9)[::-1] #signal line is 9 day EMA of MACD

    macdHistogram = [MACD[i] - signalLine[i] for i in range(numberOfPrices)] #histogram is macd - signal line

    #this preserves only the values obtained in the first call to soupToStockPrices
    stonks = [valuesList[:-numberOfPrices-1:-1] for valuesList in stonks]

    #convert unix timestamps to strings with the date and time
    stonks[0] = [datetime.utcfromtimestamp(timestamp).strftime('%m-%d-%Y %H:%M:%S') for timestamp in stonks[0]]

    #package data in a dictionary, with the most recent values at index 0 of each list
    return dict(zip(["date", "open", "high", "low", "close", "volume", "MACD", "MACD-Signal", "MACD-Hist", "error"], stonks + [MACD[:numberOfPrices], signalLine[:numberOfPrices], macdHistogram, None]))


#param: stockSymbol is a string with the symbol of the stock we're interested in      
#       startUnixTime and endUnixTime are ints containing unix timestamps of the
#           oldest and most recent stock prices we're interested in, respectively
#       interval is a string indicating how spaced out the stock prices are where it can be one of
#           H, D, W, M standing for hourly, daily, weekly, and monthly respectively
#
#return: dict with the open, low, high, close prices, volume traded, and MACD values
#           for the stock in stockSymbol from the period enclosed by startUnixTime and endUnixTime
def getStockPrices(stockSymbol, startUnixTime, endUnixTime, interval):

    #first we get the stock prices we're interested in
    #startUnixTime may be modified in getRawStockData and we need it afterwards,
    #   so we need to return it to get its current value
    stonks, startUnixTime = getRawStockData(stockSymbol, startUnixTime, endUnixTime, interval)

    #if stonks is empty, return an error
    if not stonks:
        return {'error': 'No data was obtained'}

    #then we get extra stock prices to compute the macd values more accurately
    extraStonks = getRawExtraStockData(stockSymbol, startUnixTime, interval)

    #package the requested stock information in a dictionary
    return cleanAndCombine(stonks, extraStonks)


#print(getStockPrices('aapl', 1_609_160_000-86_400, 1_609_160_000, 'H'))
