import urllib.request
import bs4 as bs
import re
import time
import ciso8601

######################################################
######################################################
##                                                  ##
##  The only functions you should call directly     ##
##  if you're testing this file are getStockPrices  ##
##  and mostRecentFiftyMACD. The rest are helpers.  ##
##  Those two are at the bottom.                    ##
##                                                  ##
######################################################
######################################################


#################################################
#################################################
#HELPER FUNCTIONS START HERE#####################
#################################################
#################################################

#param: stonksoup is the result of hitting a page with BeautifulSoup
#
#return: list of strings enclosed in span tags in the soup stonksoup
#
#Note: this is a helper function called by getSpanList which is also
#      a helper function
def soupToSpanList(stonksoup):

    spanList = []
    for stocklabel in stonksoup.find_all('span'):
        stonk = stocklabel.string
        #only adds strings to the list if they're non-null
        if stonk:
            spanList.append(stonk)

    return spanList


#param: stockSymbol is a string with the symbol of the stock we're interested in
#       startUnixTime is an int with the unix timestamp of the oldest stock price we want
#       endUnixTime is an int with the unix timestamp of the most recent stock price we want
#       interval is a string indicating how spaced out our stock prices should be
#       it can only be one of the following strings: D, W, M
#
#return: soup generated with BeautifulSoup of the page we get from the above parameters
#
#Note: this function is a helper function called by getSpanList which in turn is a
#      helper function.
def getSoup(stockSymbol, startUnixTime, endUnixTime, interval):

    #the four things that need to be filled in the yahoo finance url are the symbol
    #of the stock, and the parameters period1, period2, and interval. period1 and period2
    #must be unix timestamps indicating the oldest and most recent stock prices we want,
    #respectively. interval indicates how spaced out the stock prices should be.

    #the intervals in the yahoo finance url are 1d, 1wk, and 1mo
    #representing daily, weekly, and monthly, respectively
    interval = interval.upper()
    intervals = {"D": "1d", "W": "1wk", "M": "1mo"}

    #generate url from the above parameters
    url = 'https://finance.yahoo.com/quote/' + stockSymbol + '/history?period1=' + str(startUnixTime) + '&period2=' + str(endUnixTime) + '&interval=' + intervals[interval] + '&filter=history&frequency=1d&includeAdjustedClose=true'

    #soupify the html from the above url
    opener = urllib.request.urlopen(url).read()
    stonksoup = bs.BeautifulSoup(opener, 'lxml')

    return stonksoup


#param: stockSymbol is a string with the symbol of the stock we're interested in
#       startUnixTime is an int with the unix timestamp of the oldest stock price we want
#       endUnixTime is an int with the unix timestamp of the most recent stock price we want
#       interval is a string indicating how spaced out our stock prices should be
#       it can only be one of the following strings: D, W, M
#
#return: list of strings enclosed in span tags of the url we get from the above parameters
#
#Note: this function is a helper function called by getStockPrices and
#      mostRecentHundredClosePrices, the latter of which is also a helper function called
#      by mostRecentFiftyMACD.
def getSpanList(stockSymbol, startUnixTime, endUnixTime, interval):

    #soupify the page obtained from these four parameters
    stonksoup = getSoup(stockSymbol, startUnixTime, endUnixTime, interval)

    #gets list of strings enclosed in span tags from the soup generated above
    spanList = soupToSpanList(stonksoup)

    return spanList


#param: spanList is a list of strings enclosed in span tags
#
#return: indices which sandwich the info we need in spanList
#
#Note: this is a helper function called by setUpStockPriceLists
#      and mostRecentHundredStockPrices, both of which are helper functions
def getStartAndEndIndices(spanList):

    for i in range(len(spanList)):
        #the data starts the line after "Volume"
        if spanList[i] == "Volume":
            start = i+1

        #the data ends at the line "*Close price adjusted for splits."
        #technically it ends the line before then, but python's range
        #doesn't include the endpoint, so I set the end to be the index
        #after the end of the information
        if spanList[i] == "*Close price adjusted for splits.":
            end = i

    return start, end


#param: spanList is a list of strings enclosed in span tags. all info we need is in a span tag
#       the remaining seven arguments are lists containing info indicated by their variable names
#       this function adds to whatever info they currently have
#
#return: None. this function aims to add info to the seven lists passed as arguments
#
#Note: this is a helper function called by getStockPrices
def setUpStockPriceLists(spanList, dates, opens, highs, lows, closes, adjustedCloses, volumes):

    #this matches a date which looks like Mar 23, 2012
    #the start of each row is a date which matches this regex
    verifyDate = re.compile("[a-zA-Z]{3} \d{2}, \d{4}")

    #gets indices of spanList which sandwich the data we want
    start, end = getStartAndEndIndices(spanList)

    index = start
    while index < end:
        #each row with stock information consists of seven columns
        #in order, the columns are: Date, Open, High, Low, Close, Adjusted Close, Volume
        #if the element at the current index is a date and if the element
        #at index+7 is a date, then everything in between is info that I need
        #the same goes if the element at index is a date and if index+7 is the end of 
        #the info I need

        if verifyDate.fullmatch(spanList[index]) and (verifyDate.fullmatch(spanList[index+7]) or index+7 == end):
            #add the data to the appropriate lists
            dates.append(spanList[index])
            opens.append(spanList[index+1])
            highs.append(spanList[index+2])
            lows.append(spanList[index+3])
            closes.append(spanList[index+4])
            adjustedCloses.append(spanList[index+5])
            volumes.append(spanList[index+6])

            #set index to the next date
            index = index + 7
        else:
            #the above test will fail if there aren't seven spaces between two dates
            #this happens occassionally (you'll see something like Dividend then a number)
            #but in my experience you never miss out on stock info when you skip a row like that
            index = index + 1


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


#param: spanList is a list of strings enclosed in span tags
#       closes is a list of strings that will be filled with a stock's close prices
#       dates is a list of strings that will be filled with the dates corresponding 
#       to the prices in closes
#       start and end are the indices in spanList that sandwich the info which will
#       be stored in dates and closes
#
#return: None. this function aims to add info to dates and closes
#
#Note: this is a helper function called by mostRecentHundredClosePrices,
#      which is itself a helper function. 
def setUpHundredStockPricesList(spanList, dates, closes, start, end):

    #this matches a date which looks like Mar 23, 2012
    #the start of each row is a date which matches this regex
    verifyDate = re.compile("[a-zA-Z]{3} \d{2}, \d{4}")

    
    index = end-7
    while index >= start:
        #each row with stock information consists of seven columns
        #in order, the columns are: Date, Open, High, Low, Close, Adjusted Close, Volume
        #if the element at the current index is a date and if the element
        #at index+7 is a date, then everything in between is info that I need
        #the same goes if the element at index is a date and if index+7 is the end of 
        #the info I need

        if verifyDate.fullmatch(spanList[index]) and (verifyDate.fullmatch(spanList[index+7]) or index == end):
            #add the data to the appropriate lists
            dates.append(spanList[index])
            closes.append(spanList[index+4])

            #set index to the next date
            index = index - 7
        else:
            #the above test will fail if there aren't seven spaces between two dates
            #this happens occassionally (you'll see something like Dividend then a number)
            #but in my experience you never miss out on stock info when you skip a row like that
            index = index - 1


#param: stockSymbol is a string with the symbol of the stock we're interested in
#
#return: dict with around 100 close prices, and the dates corresponding to those prices
#        this function returns its stock prices in order from oldest to most recent, whereas
#        getStockPrices returns its stock prices from most recent to oldest. The reason for
#        this difference is that it makes the calculations in mostRecentFiftyMACD easier to write
#
#Note: this is a helper function called by mostRecentFiftyMACD
#      the idea behind this function is that it gets the maximum amount of recent
#      stock info off of one call to yahoo finance. The number of stock prices you
#      get likely won't be exactly 100, because even though we get 100 rows of data
#      from yahoo finance, some of those rows may not contain stock price info
def mostRecentHundredClosePrices(stockSymbol):

    #unix timestamp of today
    endUnixTime = int( time.time() )

    #31536000 is the number of seconds in a year 
    #I just needed a startUnixTime that was far back enough to
    #max out the number of rows in the table. The max rows is 100
    startUnixTime = endUnixTime - 31536000

    #gets list of strings enclosed in span tags in the url determined by the below parameters
    #we set the interval to D because we want daily stock price info
    spanList = getSpanList(stockSymbol, startUnixTime, endUnixTime, 'D')

    #gets indices of spanList which sandwich the data we want
    start, end = getStartAndEndIndices(spanList)

    #lists which will contain info indicated by their names
    dates, closes = [], []

    #fills in dates and closes with info from spanList in between the indices start and end
    #there is actually no reason why I should initialize dates and closes to empty lists
    #and pass them as parameters, since I can just return them from the below function
    #I did it in this way (passing them as parameters) to keep it as close to getStockPrices
    #as possible (which is the other function which does something similar to this), but
    #I'm not sure about this decision
    setUpHundredStockPricesList(spanList, dates, closes, start, end)

    #packages the lists in a single dictionary
    closesAndDates = {"Date": dates, "Close": closes}
    return closesAndDates


#param: lastHundredClosePrices is a list of strings containing
#       the most recent 100 or so close prices
#       days is an int with the number of days in the period
#
#return: float with the simple moving average of the first n values, where n is days
#        simple moving average is just the average
#
#Note: this is a helper function called by getEMA, which is also a helper function
def getSimpleMovingAverage(lastHundredClosePrices, days):

    sum = 0
    for i in range(days):
        sum += float(lastHundredClosePrices[i])
    simpleMovingAverage = sum/days

    return simpleMovingAverage


#param: lastHundredClosePrices is a list of strings containing
#       the most recent 100 or so close prices
#       days is an int with the number of days in the period
#
#return: most recent 50 values of the n period EMA, where n is days
#
#Note: this is a helper function called by mostRecentFiftyMACD
def getEMA(lastHundredClosePrices, days):

    numberOfClosePrices = len(lastHundredClosePrices)

    #calculates simple moving average of first n close prices
    simpleMovingAverage = getSimpleMovingAverage(lastHundredClosePrices, days)

    #this is the multiplier which shows up in the formula for EMA
    multiplier = 2/(1+days)

    #the first EMA is the simple moving average
    exponentialMovingAverage = simpleMovingAverage

    #calculates the EMA for the first 50 or so days
    for i in range(days, numberOfClosePrices-50):
        exponentialMovingAverage = float(lastHundredClosePrices[i])*multiplier + exponentialMovingAverage*(1-multiplier)

    #stores the last 50 EMA values in an array
    #the further we get from the simple moving average the more accurate our EMA gets,
    #so we only store the most recent 50 values (this is an arbitrary decision, but 50 is a nice number)
    EMA = []
    for i in range(numberOfClosePrices-50,numberOfClosePrices):
        exponentialMovingAverage = float(lastHundredClosePrices[i])*multiplier + exponentialMovingAverage*(1-multiplier)
        EMA.append(exponentialMovingAverage)

    return EMA


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
#return: dict with the open, low, close, adjusted close prices and volume traded
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


    #259200 is the number of seconds in three days
    #the call to get historical data only returns the most recent hundred stock prices, so I keep
    #accessing yahoo until the oldest stock price I get is within three days of the startDate
    while (startUnixTime < endUnixTime - 259200):

        #all of the info I need is enclosed in span tags
        #this returns a list of strings in span tags for the url generated by
        #the four parameters passed into this function
        spanList = getSpanList(stockSymbol, startUnixTime, endUnixTime, interval)

        #fills in the lists dates, opens, highs, lows, closes, adjustedCloses, volumes
        #with the information in spanList
        setUpStockPriceLists(spanList, dates, opens, highs, lows, closes, adjustedCloses, volumes)

        #gets the date of the oldest stock price in the most recent call to yahoo
        #and converts it to a unix timestamp. If this is within three days of the
        #startDate, the loop will end
        endUnixTime = computeNewEndUnixTime(dates[-1])


    #packages the lists in a single dictionary
    stockPriceInfo = {"Date": dates, "Open": opens, "High": highs, "Low": lows, "Close": closes, "Adjusted Close": adjustedCloses, "Volume": volumes}
    return stockPriceInfo


#param: stockSymbol is a string with the symbol of the stock we're interested in
#
#return: dict with the last fifty values of the MACD and the corresponding dates
def mostRecentFiftyMACD(stockSymbol):

    #gets dict with the most amount of recent close prices you can
    #get off of one call to yahoo finance (there will be around 100 close prices)
    closesAndDates = mostRecentHundredClosePrices(stockSymbol)

    #list of the most recent close prices, there will be around 100 of them
    lastHundredClosePrices = closesAndDates["Close"]

    #twelveDayEMA and twentySixDayEMA are lists containing the most recent 50
    #values of the 12 period and 26 period EMA, respectively
    twelveDayEMA = getEMA(lastHundredClosePrices, 12)
    twentySixDayEMA = getEMA(lastHundredClosePrices, 26)

    #MACD is a list containing the most recent 50 MACD values
    #it is the 12 Day EMA subtracted by the 26 Day EMA
    MACD = [twelveDayEMA[i] - twentySixDayEMA[i] for i in range(50)]

    #package the list of MACD values with a list of its corresponding dates
    datesAndMACD = {"Dates": closesAndDates["Date"][-50:], "MACD": MACD}

    return datesAndMACD

'''
print(getStockPrices('aapl', '2019-12-25', '1d'))
print(mostRecentFiftyMACD('aapl'))
'''
