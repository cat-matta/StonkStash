import urllib.request
from bs4 import BeautifulSoup
import time
import ciso8601

######################################################
######################################################
##                                                  ##
##  The only function you should call directly      ##
##  if you're testing this file is getStockPrices.  ##
##  The rest are helpers. That one is at the bottom ##
##                                                  ##
######################################################
######################################################


#################################################
#################################################
#HELPER FUNCTIONS START HERE#####################
#################################################
#################################################


#param: earliestDate is a string with a date which looks like Mar 23, 2012
#
#return: unix timestamp of the date in earliestDate
#
#Note: this is a helper function called by getStockPrices
def computeNewEndUnixTime(earliestDate):

    #dict where the keys are the 12 months in the form they would appear in earliestDate
    #the values are the way the months should appear in a date of the form YYYY-MM-DD
    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    #puts earliestDate in YYYY-MM-DD form
    earliestDate = earliestDate[-4:] + "-" + months[earliestDate[:3]] + "-" + earliestDate[4:6]

    #gets unix timestamp of date in earliestDate
    earliestDate = ciso8601.parse_datetime(earliestDate)
    endUnixTime = int( time.mktime( earliestDate.timetuple() ) )

    return endUnixTime


#param: value is a string containing a number
#
#return: float corresponding to the number in value. We need this because if the
#        number is greater than a thousand, there will be commas in the string
def turnFloat(value):

    #if the number is already a float we don't want to do anything
    if float != type(value):
        #deletes commas from the string, turns it into a float
        value = float( "".join( value.split(',') ) )

    return value


#param: values is a list of strings containing numbers or floats
#       we will be calculating the simple moving average of the first
#       n elements of values, where n is days
#       days is an int with the number of days in the period
#
#return: float with the simple moving average of the first n values, where n is days
#        simple moving average is just the average
#
#Note: this is a helper function called by getEMA, which is also a helper function
def getSimpleMovingAverage(values, days):

    sum = 0
    for i in range(days):
        sum += turnFloat(values[i])
    simpleMovingAverage = sum/days

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
    for i in range(days, numberOfValues):
        exponentialMovingAverage = turnFloat(values[i])*multiplier + exponentialMovingAverage*(1-multiplier)
        EMA.append(exponentialMovingAverage)

    return EMA


#param: closes is a list of strings containing all of the close prices
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
#       interval is a string, one of D, W, M, which indicates how spaced apart the stock prices should be
#
#return: soup of the html of the page containing the stock prices indicated by the parameters
def getSoup(stockSymbol, startUnixTime, endUnixTime, interval):

    interval = interval.upper()
    intervals = {"D": "1d", "W": "1wk", "M": "1mo"}

    #generate url from the above parameters
    url = f'https://finance.yahoo.com/quote/{stockSymbol}/history?period1={str(startUnixTime)}&period2={str(endUnixTime)}&interval={intervals[interval]}&filter=history&frequency=1d&includeAdjustedClose=true'

    #soupify the html from the above url
    opener = urllib.request.urlopen(url).read()
    stonksoup = BeautifulSoup(opener, 'lxml')

    return stonksoup


#param: soup is a BeautifulSoup object of the page with the stock prices we're interested in
#       the other parameters are lists of strings containing what their name suggests
#
#return: None, this function extracts the values from soup and puts them in the lists passed as parameters
def soupToStockPrices(soup, dates, opens, highs, lows, closes, adjustedCloses, volumes):

    #each row in the table is enclosed in a tr tag
    rows = soup.find_all('tr')

    #if a row has seven td tags, then it contains the information we want
    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 7:
            dates.append(columns[0].span.text)
            opens.append(columns[1].span.text)
            highs.append(columns[2].span.text)
            lows.append(columns[3].span.text)
            closes.append(columns[4].span.text)
            adjustedCloses.append(columns[5].span.text)
            volumes.append(columns[6].span.text)


#################################################
#################################################
#HELPER FUNCTIONS END HERE#######################
#################################################
#################################################


#param: stockSymbol is a string with the symbol of the stock we're interested in      
#       startDate is a string containing the oldest date of stock price you want
#       it should be in YYYY-MM-DD format
#       interval is a string indicating how spaced out the stock prices are
#       the options are D, W, M standing for daily, weekly, and monthly respectively
#
#return: dict with the open, low, close, adjusted close prices, volume traded, and MACD values
#        for the stock in stockSymbol from the startDate to now
def getStockPrices(stockSymbol, startDate, interval):

    #the url for yahoo finance requires you to fill in the parameters period1
    #and period2, which refer to the start and end of the period for which you're 
    #interested in getting stock information. These parameters only accept unix
    #timestamps, so we must convert to startDate to a unix timestamp for period1 
    #and get today's unix timestamp for period2

    #takes in the startDate in YYYY-MM-DD format and spits out the corresponding unix timestamp    
    startDate = ciso8601.parse_datetime(startDate)
    startUnixTime = int( time.mktime( startDate.timetuple() ) )

    #gets unix timestamp of now
    endUnixTime = int( time.time() )

    #list which will contain the info indicated by their names
    #they will be filled in the while loop in the call to setUpStockPriceLists
    dates, opens, highs, lows, closes, adjustedCloses, volumes = [], [], [], [], [], [], []

    #86400 is the number of seconds in one day
    #the call to get historical data only returns the most recent hundred stock prices, so I keep
    #accessing yahoo until the oldest stock price I get is within three days of the startDate if
    #the interval is daily, seven days if the interval is weekly, and thirty days if the interval
    #is monthly

    multiplier1 = {"D": 3, "W": 7, "M": 30}
    interval = interval.upper()
    spanOfTimeWhereItWouldNotMakeSenseToGetMoreStockInfo = 86400*multiplier1[interval]

    while (spanOfTimeWhereItWouldNotMakeSenseToGetMoreStockInfo < endUnixTime - startUnixTime):

        #stonksoup is a BeautifulSoup object of the page with the stock prices we want
        stonksoup = getSoup(stockSymbol, startUnixTime, endUnixTime, interval)

        #this function extracts the values from stonksoup we're interested in and puts them in the lists passed as parameters
        soupToStockPrices(stonksoup, dates, opens, highs, lows, closes, adjustedCloses, volumes)

        #gets the date of the oldest stock price in the most recent call to yahoo
        #and converts it to a unix timestamp. If this is within three days of the
        #startDate, the loop will end
        endUnixTime = computeNewEndUnixTime(dates[-1])

    #after the above loop, we have all of the stock price info we will return.
    #below this, we get extra stock prices to make the MACD values more accurate
    #and then use that information to compute the MACD values. We need to have 
    #the same amount of MACD values as stock prices, so we save the length of
    #the stock prices lists so that we can make sure that happens. Here I chose
    #to get the length of dates, which was arbitrary. I could have used any of
    #the seven lists (dates, opens, highs, etc.) since they are the same length
    numberOfStockPrices = len(dates)

    #this gives us extra stock prices before the 
    #desired start so we can get more accurate MACD values

    extraUnixTime = {'D': 15724800, 'W': 78624000, 'M': 267840000}
    extraTimeBeforeStart = startUnixTime - extraUnixTime[interval]

    #this loop functions in the same way as the one above
    while (spanOfTimeWhereItWouldNotMakeSenseToGetMoreStockInfo < endUnixTime - extraTimeBeforeStart):
        stonksoup = getSoup(stockSymbol, extraTimeBeforeStart, endUnixTime, interval)
        soupToStockPrices(stonksoup, dates, opens, highs, lows, closes, adjustedCloses, volumes)
        endUnixTime = computeNewEndUnixTime(dates[-1])

    #here we get the MACD values, signal line, and MACD histogram

    #we reverse the closes list to have the oldest stock price be at index 0
    #this makes the array slicing a bit easier and straightforward in getMACD
    MACD = getMACD(closes[::-1])

    #the signal line is the 9 day EMA of MACD
    #we reverse the MACD list to have the oldest stock price be at index 0
    #this makes the array slicing a bit easier and straightforward in getEMA
    #we also reverse the list it returns so that the most recent value is index 0
    signalLine = getEMA(MACD[::-1], 9)[::-1]

    #the MACD histogram is the MACD minus the signal line
    macdHistogram = [MACD[i] - signalLine[i] for i in range(numberOfStockPrices)]

    #packages the lists in a single dictionary
    stockPriceInfo = {"Date": dates[:numberOfStockPrices], "Open": opens[:numberOfStockPrices], "High": highs[:numberOfStockPrices], "Low": lows[:numberOfStockPrices], "Close": closes[:numberOfStockPrices], "Adjusted Close": adjustedCloses[:numberOfStockPrices], "Volume": volumes[:numberOfStockPrices], "MACD": MACD[:numberOfStockPrices], "MACD Signal Line": signalLine[:numberOfStockPrices], "MACD Histogram": macdHistogram}

    return stockPriceInfo


#print(getStockPrices('goog', '2018-12-24', 'm'))