import urllib.request
from bs4 import BeautifulSoup


'''
READ THIS BEFORE LOOKING BELOW:
All of the information we need for the app is spread across three tables in two different web pages
The five tables are labeled as: 
Assets, Liabilities, and Operating Activites
Assets and Liabilities are in the balance sheet page, Operating Activities is in the cash flow page

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


#param: assetsData, liabilitiesData, and operatingActivitiesData are lists of lists of floats
#       containing the data in the assets, liabilities, and operating activities tables, respectively
#
#return: dictionary containing all of the info which will be displayed on the balance sheet
def setUpDict(assetsData, liabilitiesData, operatingActivitiesData):

    balanceSheet = dict()

    #get info to compute ratios and compute ratios *--
    currentAssets = assetsData[19][-1]
    currentLiabilities = liabilitiesData[10][-1]
    workingCapital = currentAssets - currentLiabilities
    currentWorkingCapitalRatio = currentAssets/currentLiabilities
    inventory = assetsData[12][-1]
    quickRatio = (currentAssets - inventory)/currentLiabilities
    totalAssets = assetsData[-2][-1]
    workingCapitalOverAssets = workingCapital/totalAssets
    totalLiabilities = liabilitiesData[23][-1]
    netWorth = totalAssets - totalLiabilities
    debtWorthRatio = totalLiabilities/netWorth
    cash = assetsData[2][-1]
    cashAndShortTermInvestments = assetsData[0][-1]
    netOperatingCashFlow = operatingActivitiesData[-3][-1]
    netIncome = operatingActivitiesData[0][-1]
    flowToIncome = netOperatingCashFlow/netIncome
    threeMonthOperatingCosts = workingCapital/4
    cashOverThreeMonthOperatingCosts = cash/threeMonthOperatingCosts
    cashAndShortTermInvestmentsOverThreeMonthOperatingCosts = cashAndShortTermInvestments/threeMonthOperatingCosts
    # --*

    #put all ratios in the dict balanceSheet *--
    balanceSheet["CWC Ratio"] = {"value": currentWorkingCapitalRatio}
    balanceSheet["Quick Ratio"] = {"value": quickRatio}
    balanceSheet["Working Capital Over Assets"] = {"value": workingCapitalOverAssets}
    balanceSheet["Debt Worth Ratio"] = {"value": debtWorthRatio}
    balanceSheet["Flow to Income"] = {"value": flowToIncome}
    balanceSheet["Cash Over 3 Month Operating Costs"] = {"value": cashOverThreeMonthOperatingCosts}
    balanceSheet["C&ST Over TMOC"] = {"value": cashAndShortTermInvestmentsOverThreeMonthOperatingCosts}
    # --*

    #figure out which ratios should be flagged *--
    balanceSheet["CWC Ratio"]["isFlagged"] = True if currentWorkingCapitalRatio < 1.2 else False
    balanceSheet["Quick Ratio"]["isFlagged"] = True if quickRatio < 1 else False
    balanceSheet["Working Capital Over Assets"]["isFlagged"] = True if workingCapitalOverAssets < .12 or workingCapitalOverAssets > .3 else False
    balanceSheet["Debt Worth Ratio"]["isFlagged"] = True if debtWorthRatio >= 1 else False
    balanceSheet["Flow to Income"]["isFlagged"] = True if netIncome < 0 or netOperatingCashFlow < 0 or flowToIncome < 1 else False
    balanceSheet["Cash Over 3 Month Operating Costs"]["isFlagged"] = True if cashOverThreeMonthOperatingCosts < 1 else False
    balanceSheet["C&ST Over TMOC"]["isFlagged"] = True if cashAndShortTermInvestmentsOverThreeMonthOperatingCosts < 4 else False
    # --*

    return balanceSheet


#param: stockSymbol is a string containing the symbol of the stock we're interested in
#
#return: two soup objects with the balance sheet and cash flow pages of the stock on marketwatch
def getSoup(stockSymbol):
    #an f before the string allows us to use string interpolation ({stockSymbol})
    balanceSheetUrl = f"https://www.marketwatch.com/investing/stock/{stockSymbol}/financials/balance-sheet/quarter"
    cashFlowUrl = f"https://www.marketwatch.com/investing/stock/{stockSymbol}/financials/cash-flow/quarter"

    balanceSheetHtml, cashFlowHtml = urllib.request.urlopen(balanceSheetUrl).read(), urllib.request.urlopen(cashFlowUrl).read()

    return BeautifulSoup(balanceSheetHtml, 'lxml'), BeautifulSoup(cashFlowHtml, 'lxml')


#param: stockSymbol is a string containing the symbol of the desired stock
#
#return: dictionary containing all of the balance sheet info of the stock in stockSymbol
def driver(stockSymbol):

    balanceSheetSoup, cashFlowSoup = getSoup(stockSymbol)

    #the tables containing our information have the css class "table table--overflow align--right"
    #balanceSheetTables is a list of the html of the two tables on the balance sheet page: assets and liabilities
    balanceSheetTables = balanceSheetSoup.find_all(class_ = "table table--overflow align--right")

    #this contains the html of the operating activities table on the cash flow page
    operatingActivitiesTable = cashFlowSoup.find(class_ = "table table--overflow align--right")

    assetsData = [[float(value) for value in row["data-chart-data"].split(',') if value != ''] for row in balanceSheetTables[0].find_all(class_ = "chart--financials js-financial-chart")]

    liabilitiesData = [[float(value) for value in row["data-chart-data"].split(',') if value != ''] for row in balanceSheetTables[1].find_all(class_ = "chart--financials js-financial-chart")]

    operatingActivitiesData = [[float(value) for value in row["data-chart-data"].split(',') if value != ''] for row in operatingActivitiesTable.find_all(class_ = "chart--financials js-financial-chart")]


    #setUpDict takes in the above five dictionaries, extracts the information we need,
    #and packages it in a single dictionary which we return
    return setUpDict(assetsData, liabilitiesData, operatingActivitiesData)


#uncomment below to run this file by itself
#print(driver('gme'))