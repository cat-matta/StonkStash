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
        stonk = stocklabel.string
        if stonk:
            divList.append(stonk)

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

    #get info to compute ratios and compute ratios *--
    currentAssets = turnFloat(assets["Total Current Assets"][4])
    currentLiabilities = turnFloat(liabilities["Total Current Liabilities"][4])
    workingCapital = currentAssets - currentLiabilities
    currentWorkingCapitalRatio = currentAssets/currentLiabilities
    inventory = turnFloat(assets["Inventories"][4])
    quickRatio = (currentAssets - inventory)/currentLiabilities
    totalAssets = turnFloat(assets["Total Assets"][4])
    workingCapitalOverAssets = workingCapital/totalAssets
    totalLiabilities = turnFloat(liabilities["Total Liabilities"][4])
    netWorth = totalAssets - totalLiabilities
    debtWorthRatio = totalLiabilities/netWorth
    cash = turnFloat(assets["Cash Only"][4])
    cashAndShortTermInvestments = turnFloat(assets["Cash & Short Term Investments"][4])
    netOperatingCashFlow = turnFloat(operating["Net Operating Cash Flow"][4])
    netIncome = turnFloat(operating["Net Income before Extraordinaries"][4])
    flowToIncome = netOperatingCashFlow/netIncome
    threeMonthOperatingCosts = workingCapital/4
    cashOverThreeMonthOperatingCosts = cash/threeMonthOperatingCosts
    cashAndShortTermInvestmentsOverThreeMonthOperatingCosts = turnFloat(assets["Cash & Short Term Investments"][4])/threeMonthOperatingCosts
    # --*

    #put all ratios in the dict balanceSheet *--
    #ratios are not flagged by default
    balanceSheet["CWC Ratio"] = {"value": currentWorkingCapitalRatio, "isFlagged": False}
    balanceSheet["Quick Ratio"] = {"value": quickRatio, "isFlagged": False}
    balanceSheet["Working Capital Over Assets"] = {"value": workingCapitalOverAssets, "isFlagged": False}
    balanceSheet["Debt Worth Ratio"] = {"value": debtWorthRatio, "isFlagged": False}
    balanceSheet["Flow to Income"] = {"value": flowToIncome, "isFlagged": False}
    balanceSheet["Cash Over 3 Month Operating Costs"] = {"value": cashOverThreeMonthOperatingCosts, "isFlagged": False}
    balanceSheet["C&ST Over TMOC"] = {"value": cashAndShortTermInvestmentsOverThreeMonthOperatingCosts, "isFlagged": False}
    # --*


    #figure out which ratios should be flagged *--
    if currentWorkingCapitalRatio < 1.2:
        balanceSheet["CWC Ratio"]["isFlagged"] = True

    if quickRatio < 1:
        balanceSheet["Quick Ratio"]["isFlagged"] = True

    if workingCapitalOverAssets < .12 or workingCapitalOverAssets > .3:
        balanceSheet["Working Capital Over Assets"]["isFlagged"] = True

    if debtWorthRatio >= 1:
        balanceSheet["Debt Worth Ratio"]["isFlagged"] = True

    if netIncome < 0 or netOperatingCashFlow < 0 or flowToIncome < 1:
        balanceSheet["Flow To Income"]["isFlagged"] = True

    if cashOverThreeMonthOperatingCosts < 1:
        balanceSheet["Cash Over 3 Month Operating Costs"]["isFlagged"] = True

    if cashAndShortTermInvestmentsOverThreeMonthOperatingCosts < 4:
        balanceSheet["C&ST Over TMOC"]["isFlagged"] = True
    # --*

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
#print(driver('aapl'))