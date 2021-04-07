import urllib.request
import bs4 as bs
import re
import time
import ciso8601

######################################################
######################################################
##                                                  ##
##  The only function you should call directly      ##
##  if you're testing this file is getStockPrices   ##
##  The rest are helpers. That one is at the bottom ##
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
#Note: this function is a helper function called by getStockPrices
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
#      which is a helper functions
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


#param: closes is a list of strings containing all of the close prices 
#       of the stock in the period we're interested in
#       days is an int with the number of days in the period
#
#return: float with the simple moving average of the first n values, where n is days
#        simple moving average is just the average
#
#Note: this is a helper function called by getEMA, which is also a helper function
def getSimpleMovingAverage(closes, days):

    sum = 0
    for i in range(days):
        sum += float(closes[i])
    simpleMovingAverage = sum/days

    return simpleMovingAverage

#param: closes is a list of strings containing all of the close prices
#       of the stock in the period we're interested in
#       days is an int with the number of days in the period
#       numberOfValuesToReturn is an int with the length of the EMA list we return
#
#return: list with EMA values, the amount of which is indicated by numberOfValuesToReturn
#
#Note: this is a helper function called by getMACD, which is also a helper function
def getEMA(closes, days, numberOfValuesToReturn):

    #the strategy here is to calculate all of the EMA values we can,
    #but we only return the most recent n number of values, where 
    #n is numberOfValuesToReturn

    #numberOfEMAvaluesToComputeWithoutStoring tells us how many close
    #prices we go through to compute the EMA without storing them
    numberOfClosePrices = len(closes)
    numberOfEMAvaluesToComputeWithoutStoring = numberOfClosePrices - numberOfValuesToReturn

    #the initial EMA value can be taken to be the simple moving average
    #(EMA is defined recursively, so we need a base case. That base case is the SMA)
    exponentialMovingAverage = getSimpleMovingAverage(closes, days)

    #this multiplier is a part of the formula
    multiplier = 2/(1+days)

    #this loop computes all of the EMA values we won't return
    for i in range(days, numberOfEMAvaluesToComputeWithoutStoring):
        exponentialMovingAverage = float(closes[i])*multiplier + exponentialMovingAverage*(1-multiplier)

    #this loop computes all of the EMA values we will return
    EMA = []
    for i in range(numberOfEMAvaluesToComputeWithoutStoring, numberOfClosePrices):
        exponentialMovingAverage = float(closes[i])*multiplier + exponentialMovingAverage*(1-multiplier)
        EMA.append(exponentialMovingAverage)

    return EMA


#param: closes is a list of strings containing all of the close prices
#       numberOfValuesToReturn is the length of the list of MACD values we're returning
#
#return: list of MACD values, the length of which is indicated by numberOfValuesToReturn
#
#Note: this is a helper function called by getStockPrices
def getMACD(closes, numberOfValuesToReturn):

    #twelveDayEMA and twentySixDayEMA are lists with the 12 and 26 day EMA's
    #respectively, and the length of those lists are indicated by numberOfValuesToReturn
    twelveDayEMA = getEMA(closes, 12, numberOfValuesToReturn)
    twentySixDayEMA = getEMA(closes, 26, numberOfValuesToReturn)

    #MACD is 12 day EMA - 26 day EMA
    MACD = [twelveDayEMA[i] - twentySixDayEMA[i] for i in range(numberOfValuesToReturn)]

    #I reverse MACD so that the most recent values are at index 0
    #this is to match the other lists which will go in the dict
    #which will be returned in getStockPrices
    return MACD[::-1]


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

    #after the above loop, we have all of the stock price info we will return
    #below this, we get another half year's worth of stock prices to make the 
    #MACD values more accurate and then use that information to compute the MACD 
    #values. We need to have the same amount of MACD values as stock prices,
    #so we save the length of the stock prices lists so that we can make sure 
    #that happens. Here I chose to get the length of dates, which was arbitrary.
    #I could have used any of the seven lists (dates, opens, highs, etc.) since 
    #they are the same length
    numberOfStockPrices = len(dates)

    #this gives us half a year of extra stock prices before the desired start
    #so we can get more accurate MACD values
    unixTimeHalfYearBeforeStart = startUnixTime - 15724800

    #this loop functions in the same way as the one above
    while (unixTimeHalfYearBeforeStart < endUnixTime - 259200):
        spanList = getSpanList(stockSymbol, unixTimeHalfYearBeforeStart, endUnixTime, interval)
        setUpStockPriceLists(spanList, dates, opens, highs, lows, closes, adjustedCloses, volumes)
        endUnixTime = computeNewEndUnixTime(dates[-1])

    #getMACD returns a list of MACD values, the length of which is numberOfStockPrices
    #I reverse closes so that the oldest price are at index 0. This makes the string
    #slicing in getMACD a bit easier and straightforward.
    MACD = getMACD(closes[::-1], numberOfStockPrices)

    #packages the lists in a single dictionary
    stockPriceInfo = {"Date": dates[:numberOfStockPrices], "Open": opens[:numberOfStockPrices], "High": highs[:numberOfStockPrices], "Low": lows[:numberOfStockPrices], "Close": closes[:numberOfStockPrices], "Adjusted Close": adjustedCloses[:numberOfStockPrices], "Volume": volumes[:numberOfStockPrices], "MACD": MACD[:numberOfStockPrices]}

    return stockPriceInfo


#print(getStockPrices('gme', '2019-12-24', 'd'))