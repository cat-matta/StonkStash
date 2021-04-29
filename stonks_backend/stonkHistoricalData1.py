import requests
import json
from datetime import datetime
import time

####FUNCTION SIGNATURES###############################################
#                                                                   ##
# getPageContent(ticker, interval, span)                            ##
# getStockPrices(stockSymbol, interval, span)                       ##
#                                                                   ##
######################################################################


#param: ticker is a string containing the symbol of the stock we're interested in
#       interval is a string containing how spaced out consecutive stock prices are
#       span is a string containing the period of time we're trying to find stock prices for
#       interval and span are intervals following the ISO 8601 standard
#       to see how they should be written, go to https://en.wikipedia.org/wiki/ISO_8601#Time_intervals
#       they should be written like point 4 in the list in the "Time intervals" subheading
#
#return: dictionary containing the data in the page with the info we want
#
#Note: this is a helper function called by getStockPrices
def getPageContent(ticker, interval, span):

    #the api call is a post request to the following url
    url = "https://api-secure.wsj.net/api/michelangelo/timeseries/history?hash=1945186257&ckey=cecc4267a0"

    #we have to pass a json with all of our desired settings.
    #setting Step to interval, TimeFrame to span, and Key to ticker are absolutely necessary
    #I'm not sure what all of the settings do, but I specifically set ShowPreMarket and ShowAfterHours to True
    #to get as much data as possible, and FilterNullSlots to True to avoid getting null values
    jso = {"Step":interval,"TimeFrame":span,"EntitlementToken":"cecc4267a0194af89ca343805a3e57af","IncludeMockTick":True,"FilterNullSlots":True,"FilterClosedPoints":True,"IncludeClosedSlots":False,"IncludeOfficialClose":True,"InjectOpen":False,"ShowPreMarket":True,"ShowAfterHours":True,"UseExtendedTimeFrame":True,"WantPriorClose":False,"IncludeCurrentQuotes":False,"ResetTodaysAfterHoursPercentChange":False,"Series":[{"Key":ticker,"Dialect":"Charting","Kind":"Ticker","SeriesId":"s1","DataTypes":["Open","High","Low","Last"],"Indicators":[{"Parameters":[{"Name":"Period","Value":"50"}],"Kind":"SimpleMovingAverage","SeriesId":"i2"},{"Parameters":[],"Kind":"Volume","SeriesId":"i3"},{"Parameters":[{"Name":"EMA1","Value":12},{"Name":"EMA2","Value":26},{"Name":"SignalLine","Value":9}],"Kind":"MovingAverageConvergenceDivergence","SeriesId":"i4"},{"Parameters":[{"Name":"YearOverYear"}],"Kind":"EarningsEvents","SeriesId":"i5"},{"Parameters":[],"Kind":"DividendEvents","SeriesId":"i6"},{"Parameters":[],"Kind":"SplitEvents","SeriesId":"i7"}]}]}

    #I set these headers to emulate the request sent by my browser as closely as possible
    #I would imagine that the only ones that actually matter are Dylan2010.EntitlementToken
    #and maybe the Host, Origin, and Referer, but I haven't yet tried deleting them one by one
    #to see which are truly necessary
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/json; charset=utf-8',
        'Origin': 'https://www.marketwatch.com',
        'Content-Length': '1100',
        'Accept-Language': 'en-us',
        'Host': 'api-secure.wsj.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Referer': 'https://www.marketwatch.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Dylan2010.EntitlementToken': 'cecc4267a0194af89ca343805a3e57af'
    }

    page = requests.post(url, headers=headers, json=jso)
    return json.loads(page.content)


#param: ticker is a string containing the symbol of the stock we're interested in
#       interval is a string containing how spaced out consecutive stock prices are
#       span is a string containing the period of time we're trying to find stock prices for
#       interval and span are intervals following the ISO 8601 standard
#       to see how they should be written, go to https://en.wikipedia.org/wiki/ISO_8601#Time_intervals
#       they should be written like point 4 in the list in the "Time intervals" subheading
#
#return: dict with the dates, open, high, low, and close prices, volume traded, 
#         and macd, macd signal, and macd histogram values.
def getStockPrices(ticker, interval, span):

    #info is a dict with all of the date on the page with the information we want
    info = getPageContent(ticker, interval, span)

    #timestamps, these are unix timestamps in milliseconds, not in seconds
    times = info["TimeInfo"]["Ticks"]

    #this is the number of stock prices we get
    #I thought this might be useful info, but I don't do anything with it
    numOfPrices = info["TimeInfo"]["TickCount"]

    #this is a list whose length is numOfPrices, and each element is a list where
    #the elements are the open, high, low, and close prices in that order. The element
    #at index i of stockPrices are the stock prices at the timestamp at index i of times
    stockPrices = info["Series"][0]["DataPoints"]

    #this is a list whose length is numOfPrices, and each element is a list with one element,
    #the volume of stocks traded. The element at index i of volumes is the volume of stocks traded
    #at the timestamp at index i of times
    volumes = info["Series"][2]["DataPoints"]

    #this turns the volumes into a list of floats instead of a list of lists
    volumes = [volume[0] for volume in volumes]

    #this is a list of strings containing the strings MACD, MACD-Signal, and MACD-Hist
    #the order in which those strings appear in the list macdNames is the same as the
    #order in which their corresponding values will appear in the list macdInfo
    macdNames = info["Series"][3]["DesiredDataPoints"]

    #this is a list whose length is numOfPrices, and each element is a list containing
    #macd, macd signal, and macd histogram values. the three values at index i of macdInfo
    #are the macd values at the timestamp at index i of times
    macdInfo = info["Series"][3]["DataPoints"]

    #converts the unix timestamps to strings containing their corresponding date and time
    dates = [datetime.utcfromtimestamp(time//1000).strftime('%m-%d-%Y %H:%M:%S') for time in times]

    return dict( zip(["date", "open", "high", "low", "close", "volume", *macdNames], [dates[::-1]] + [[stock[i] for stock in stockPrices][::-1] for i in range(4)] + [volumes[::-1]] + [[macd[i] for macd in macdInfo][::-1] for i in range(3)]) )
    