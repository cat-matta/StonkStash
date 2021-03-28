import urllib.request
import bs4 as bs
import re


'''
READ THIS BEFORE LOOKING BELOW:
All of the information we need for the app is spread across five tables in two different web pages
The five tables are labeled as: 
Assets, Liabilities, Operating Activites, Investing Activities, and Financing Activities
Assets and Liabilities are in the balance sheet page, the other three are in the cash flow page

REMEMBER: Assets and Liabilities are in the balance sheet page
Operating Activities, Investing Activites, and Financing Activites are in the cash flow page
'''

#################################################
#################################################
##                                             ##
##  the driver function is the magic, the rest ##
##  are methods which are called by it         ##
##                                             ##
#################################################
#################################################


#param: url is a string containing a URL which has info we need
#
#return: list of strings contained in the div tags of the above url
def getDivListHelper(url):

    #get url and soupify it (helps us parse)
    opener = urllib.request.urlopen(url).read()
    stonksoup = bs.BeautifulSoup(opener,'lxml')

    #puts all non-null strings in a div tag in divList
    divList = []
    for stocklabel in stonksoup.find_all('div'):
        if stocklabel.string:
            divList.append(stocklabel.string)

    return divList


#param: stockSymbol is a string containing the symbol of the desired stock
#
#return: two lists of strings
#        balanceList is a list of strings contained in the div tags on the stock's balance sheet page
#        cashFlowList is a list of strings contained in the div tags on the stock's cash flow page
def getDivList(stockSymbol):

    #urls containing all of the info we need
    balanceLink = 'https://www.marketwatch.com/investing/stock/' + stockSymbol + '/financials/balance-sheet/quarter'
    cashLink = 'https://www.marketwatch.com/investing/stock/' + stockSymbol + '/financials/cash-flow/quarter'

    #obtain list of strings contained in the div tags of the above urls
    balanceList = getDivListHelper(balanceLink)
    cashList = getDivListHelper(cashLink)

    return balanceList, cashList


#param: divList is either balanceList or cashFlowList
#       it takes in a list of strings inside div tags
#       start and end are the indices in divList which sandwich
#       the table whose information we are obtaining
#
#return: dictionary containing all info in the table whose last row has the heading finalRow
#
#note: this function is called by infoToDict
def infoToDictHelper(divList, start, end):

    tableInfo = {}

    #each row consists of seven elements in divList
    #the first two are the heading of the row repeated
    #the next five are the values corresponding to that heading,
    #with the final value being the most recent 

    #counter1 keeps track of where we are in the pattern of seven
    counter1 = 0

    #counter2 keeps track of where we are in the five values of the row
    #when it is -1, we are on the heading (so we are not on one of the five values)
    counter2 = -1

    for i in range(start, end):

        #if counter1 is 0, we are on the first element of the row, so this is the heading
        if counter1 == 0:
            heading = divList[i]

            #creates an empty list corresponding to the heading
            tableInfo[heading] = []

        #if counter1 is 2, then we are on the first of the five values
        if counter1 == 2:
            counter2 = 0

        #if counter2 is 5, then we are at the end of the row, 
        #so we reset it to its original value
        if counter2 == 5:
            counter2 = -1

        #if counter2 is not -1, then we are on the values of the row, 
        #so we append the current item to the current heading's list
        if counter2 != -1:
            tableInfo[heading].append(divList[i])
            counter2 = counter2 + 1

        counter1 = counter1 + 1
        #if counter1 is 7, we are at the end of the row, 
        #so we reset it to its original value
        if counter1 == 7:
            counter1 = 0

    return tableInfo


#param: divList is either balanceList or cashFlowList
#       it takes in a list of strings inside div tags
#       finalRow is a string containing the title of the last row in the table
#return: dictionary containing all info in the table whose last row has the heading finalRow
def infoToDict(divList, finalRow):

    #regex saying that something is in the form of a date
    #the start of each table is a date, so this regex verifies that the line is a date
    verifyDate = re.compile("(\d{2})-([a-zA-Z]{3})-(\d{4})")

    for i in range(len(divList)):
        #the start of the table is always 6 lines after a date which comes after a line saying "Item"
        if divList[i] == "Item":
            if verifyDate.fullmatch(divList[i+1]):
                start = i+7

        #the final piece of info in the table is always seven lines after the finalRow
        if divList[i] == finalRow:
            end = i+7
            break

    #infoToDictHelper returns a dictionary with all of the info in the table whose last
    #row has the heading finalRow. start and end are the indices in divList which sandwich
    #the table's information
    return infoToDictHelper(divList, start, end)


#param: value is a string containing a number that will appear on the balance sheet
#       the number, if it is larger than a million, will end in either an M or a B
#       to indicate millions or billions respectively
#       if it is negative, it will be enclosed in parenthesis ()
#
#return: float equal to the number indicated by value
def turnFloat(value):
    #by default value is positive
    #(I know parity refers to even or odd but it feels right here)
    parity = 1

    #it's negative if it's enclosed by parenthesis
    if value[0] == '(':
        #cuts off parenthesis and sets the number to negative
        value = value[1:-1]
        parity = -1

    #if the number ends in K, M, or B, multiply the numeric value by a million or billion, respectively
    multiplier = 1
    multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    lastChar = value[-1]
    if lastChar in multipliers:
        multiplier = multipliers[lastChar]
        value = value[:-1]

    #actual number is the value times the multiplier times whether it's positive or negative
    value = float(value)
    return value*multiplier*parity


#param: assets is a dictionary containing the info in the Assets table
#       liabilities is a dictionary containing the info in the Liabilities table
#       operating is a dictionary containing the info in the Operating Activities table
#       investing is a dictionary containing the info in the Investing Activities table
#       financing is a dictionary containing the info in the Financing Activities table
#
#return: dictionary containing all of the info which will be displayed on the balance sheet
def setUpDict(assets, liabilities, operating, investing, financing):

    balanceSheet = dict()

    #put all data we need in the dict balanceSheet *--
    balanceSheet["Current Assets"] = turnFloat(assets["Total Current Assets"][4])
    balanceSheet["Current Liabilities"] = turnFloat(liabilities["Total Current Liabilities"][4])
    balanceSheet["Working Capital"] = balanceSheet["Current Assets"] - balanceSheet["Current Liabilities"]
    balanceSheet["CWC Ratio"] = balanceSheet["Current Assets"]/balanceSheet["Current Liabilities"]
    balanceSheet["Inventory"] = turnFloat(assets["Inventories"][4])
    balanceSheet["Quick Ratio"] = (balanceSheet["Current Assets"] - balanceSheet["Inventory"])/balanceSheet["Current Liabilities"]
    balanceSheet["Total Assets"] = turnFloat(assets["Total Assets"][4])
    balanceSheet["Working Capital Over Assets"] = balanceSheet["Working Capital"]/balanceSheet["Total Assets"]
    balanceSheet["Total Liabilities"] = turnFloat(liabilities["Total Liabilities"][4])
    balanceSheet["Net Worth"] = balanceSheet["Total Assets"] - balanceSheet["Total Liabilities"]
    balanceSheet["Debt Worth Ratio"] = balanceSheet["Total Liabilities"]/balanceSheet["Net Worth"]
    balanceSheet["Cash"] = turnFloat(assets["Cash Only"][4])
    balanceSheet["Cash and Short Term Investments"] = turnFloat(assets["Cash & Short Term Investments"][4])
    balanceSheet["Net Operating Cash Flow"] = turnFloat(operating["Net Operating Cash Flow"][4])
    balanceSheet["Net Income"] = turnFloat(operating["Net Income before Extraordinaries"][4])
    balanceSheet["Flow to Income"] = balanceSheet["Net Operating Cash Flow"]/balanceSheet["Net Income"]
    balanceSheet["3 Month Operating Costs"] = balanceSheet["Working Capital"]/4
    balanceSheet["Cash Over 3 Month Operating Costs"] = turnFloat(assets["Cash Only"][4])/balanceSheet["3 Month Operating Costs"]
    balanceSheet["C&ST Over TMOC"] = turnFloat(assets["Cash & Short Term Investments"][4])/balanceSheet["3 Month Operating Costs"]
    # --*


    #figure out which ratios are ideal, and which should be flagged *--
    ideals = []
    flags = []
    if balanceSheet["CWC Ratio"] < 1.2:
        flags.append("Current Working Capital Ratio")
    else:
        ideals.append("Current Working Capital Ratio")

    if balanceSheet["Quick Ratio"] < 1:
        flags.append("Quick Ratio")
    else:
        ideals.append("Quick Ratio")

    if balanceSheet["Working Capital Over Assets"] < .12 or balanceSheet["Working Capital Over Assets"] > .3:
        flags.append("Working Capital over Assets")
    else:
        ideals.append("Working Capital over Assets")

    if balanceSheet["Debt Worth Ratio"] < 1:
        ideals.append("Debt Worth Ratio")
    else:
        flags.append("Debt Worth Ratio")

    if balanceSheet["Net Income"] < 0 or balanceSheet["Net Operating Cash Flow"] < 0 or balanceSheet["Flow to Income"] < 1:
        flags.append("Net Operating Cash Flow to Net Income")
    else:
        ideals.append("Net Operating Cash Flow to Net Income")

    if balanceSheet["Cash Over 3 Month Operating Costs"] < 1:
        flags.append("Cash over 3-Month Operating Costs")
    else:
        ideals.append("Cash over 3-Month Operating Costs")

    if balanceSheet["C&ST Over TMOC"] < 4:
        flags.append("Cash and Short Term Investments over 3-Month Operating Costs")
    else:
        ideals.append("Cash and Short Term Investments over 3-Month Operating Costs")
    # --*

    #puts the ratios which are ideal and which should be flagged
    #in the dictionary balanceSheet
    balanceSheet["flags"] = flags
    balanceSheet["ideals"] = ideals

    return balanceSheet


#param: stockSymbol is a string containing the symbol of the desired stock
#
#return: dictionary containing all of the balance sheet info of the stock in stockSymbol
def driver(stockSymbol):

    #lists containing all of the strings in div tags
    #balanceList refers to the info on the balance sheet page
    #cashFlowList refers to the info on the cash flow page
    balanceList, cashFlowList = getDivList(stockSymbol)


    #assets, liabilities, operating, investing, and financing are dictionaries containining
    #all of the info in the five tables Assets, Liabilities, Operating Activities,
    #Investing Activities, and Financing Activities respectively

    #the Assets table is in the balance sheet page, 
    #and the last line of the table is "Total Assets Growth"
    assets = infoToDict(balanceList, "Total Assets Growth")

    #the Liabilities table is in the balance sheet page,
    #and the last line of the table is "Liabilities & Shareholders' Equity"
    liabilities = infoToDict(balanceList, "Liabilities & Shareholders' Equity")

    #the Operating Activities table is in the cash flow page,
    #and the last line of the table is "Net Operating Cash Flow / Sales"
    operating = infoToDict(cashFlowList, "Net Operating Cash Flow / Sales")

    #the Investing Activities table is in the cash flow page,
    #and the last line of the table is "Net Investing Cash Flow / Sales"
    investing = infoToDict(cashFlowList, "Net Investing Cash Flow / Sales")

    #the Financing Activities table is in the cash flow page,
    #and the last line of the table is "Free Cash Flow Yield"
    financing = infoToDict(cashFlowList, "Free Cash Flow Yield")


    #setUpDict takes in the above five dictionaries, extracts the information we need,
    #and packages it in a single dictionary which we return
    return setUpDict(assets, liabilities, operating, investing, financing)


#uncomment below to run this file by itself
print(driver('aapl'))