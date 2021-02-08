import pandas as pd
import urllib as urlpull
import urllib.request
import bs4 as bs
import re

#EVERYTHING HAPPENS IN THE driver() FUNCTION AT THE BOTTOM

def getDivListHelper(url):
    opener = urllib.request.urlopen(url).read() ##opens the html page
    stonksoup = bs.BeautifulSoup(opener,'lxml')
    divList = [] ##create a list to add anything with the div tag
    for stocklabel in stonksoup.find_all('div'):
        if stocklabel.string:
            divList.append(stocklabel.string)

    return divList

def getDivList(stockSymbol):
    balanceLink = 'https://www.marketwatch.com/investing/stock/' + stockSymbol + '/financials/balance-sheet/quarter'
    cashLink = 'https://www.marketwatch.com/investing/stock/' + stockSymbol + '/financials/cash-flow/quarter'
    balanceList = getDivListHelper(balanceLink)
    cashList = getDivListHelper(cashLink)
    return balanceList, cashList

def getIndices(divList, finalRow, verifyDate):
    for i in range(len(divList)):
        if divList[i] == "Item":
            if verifyDate.fullmatch(divList[i+1]):
                start = i+1

        if divList[i] == finalRow:
            end = i+7
            break

    return start, end

def infoToDict(divList, start, end):
    diction = {}
    counter1 = 0
    counter2 = -1
    for i in range(start+6, end):

        if counter1 == 0:
            heading = divList[i]
            diction[heading] = []

        if counter1 == 2:
            counter2 = 0

        if counter2 == 5:
            counter2 = -1

        if counter2 != -1:
            diction[heading].append(divList[i])
            counter2 = counter2 + 1

        counter1 = counter1 + 1
        if counter1 == 7:
            counter1 = 0

    return diction

def turnFloat(value):
    parity = 1
    if value[0] == '(':
        value = value[1:-1]
        parity = -1
    multiplier = 1
    if value[-1] == 'M':
        multiplier = 1000000
    if value[-1] == 'B':
        multiplier = 1000000000
    value = value[:-1]
    value = float(value)
    return value*multiplier*parity

def driver():
    #put in the stock symbol you want
    stockSymbol = 'aapl'

    #lists containing all of the strings in div tags
    balanceList, cashFlowList = getDivList(stockSymbol)

    #regex saying that something is in the form of a date
    verifyDate = re.compile("(\d{2})-([a-zA-Z]{3})-(\d{4})")

    #indices of the lists which sandwich the info we need
    startAssets, endAssets = getIndices(balanceList, "Total Assets Growth", verifyDate)
    startLiabilities, endLiabilities = getIndices(balanceList, "Liabilities & Shareholders' Equity", verifyDate)
    startOperatingActivities, endOperatingActivities = getIndices(cashFlowList, "Net Operating Cash Flow / Sales", verifyDate)
    startInvestingActivities, endInvestingActivities = getIndices(cashFlowList, "Net Investing Cash Flow / Sales", verifyDate)
    startFinancingActivities, endFinancingActivities = getIndices(cashFlowList, "Free Cash Flow Yield", verifyDate)

    #dictionaries containing the info we need in a nice format
    assets = infoToDict(balanceList, startAssets, endAssets)
    liabilities = infoToDict(balanceList, startLiabilities, endLiabilities)
    operating = infoToDict(cashFlowList, startOperatingActivities, endOperatingActivities)
    investing = infoToDict(cashFlowList, startInvestingActivities, endInvestingActivities)
    financing = infoToDict(cashFlowList, startFinancingActivities, endFinancingActivities)

    #all of the info asked for
    currentAssets = turnFloat(assets["Total Current Assets"][4])
    currentLiabilities = turnFloat(liabilities["Total Current Liabilities"][4])
    workingCapital = currentAssets - currentLiabilities
    cwcRatio = currentAssets/currentLiabilities
    inventory = turnFloat(assets["Inventories"][4])
    quickRatio = (currentAssets - inventory)/currentLiabilities
    totalAssets = turnFloat(assets["Total Assets"][4])
    wcOverAssets = workingCapital/totalAssets
    totalLiabilities = turnFloat(liabilities["Total Liabilities"][4])
    netWorth = totalAssets - totalLiabilities
    debtWorthRatio = totalLiabilities/netWorth
    cash = turnFloat(assets["Cash Only"][4])
    cANDst = turnFloat(assets["Cash & Short Term Investments"][4])
    freeCashFlow = turnFloat(operating["Net Operating Cash Flow"][4])
    netIncome = turnFloat(operating["Net Income before Extraordinaries"][4])
    flowToIncome = freeCashFlow/netIncome
    tmoc = workingCapital/4
    cashOverTMOC = cash/tmoc
    castOverTMOC = cANDst/tmoc
    
    #uncomment below to see the values
    
    print("Current Assets: " + str(currentAssets))
    print("Current Liabilities: " + str(currentLiabilities))
    print("Working Capital: " + str(workingCapital))
    print("Current Working Capital Ratio: " + str(cwcRatio))
    print("Inventory: " + str(inventory))
    print("Quick Ratio: " + str(quickRatio))
    print("Total Assets: " + str(totalAssets))
    print("Working Capital Over Assets: " + str(wcOverAssets))
    print("Total Liabilities: " + str(totalLiabilities))
    print("Net Worth: " + str(netWorth))
    print("Debt Worth Ratio: " + str(debtWorthRatio))
    print("Cash: " + str(cash))
    print("Cash and Short Term Investments: " + str(cANDst))
    print("Net Operating Cash Flow: " + str(freeCashFlow))
    print("Net Income: " + str(netIncome))
    print("Flow to Income: " + str(flowToIncome))
    print("3 Month Operating Costs: " + str(tmoc))
    print("Cash over 3 Month Operating Costs: " + str(cashOverTMOC))
    print("Cash and Short Term Investments over 3 Month Operating Costs: " + str(castOverTMOC))
    

    ideals = []
    flags = []
    if cwcRatio < 1.2:
        flags.append("Current Working Capital Ratio")
    else:
        ideals.append("Current Working Capital Ratio")

    if quickRatio < 1:
        flags.append("Quick Ratio")
    else:
        ideals.append("Quick Ratio")

    if wcOverAssets < .12 or wcOverAssets > .3:
        flags.append("Working Capital over Assets")
    else:
        ideals.append("Working Capital over Assets")

    if debtWorthRatio < 1:
        ideals.append("Debt Worth Ratio")
    else:
        flags.append("Debt Worth Ratio")

    if netIncome < 0 or freeCashFlow < 0 or flowToIncome < 1:
        flags.append("Net Operating Cash Flow to Net Income")
    else:
        ideals.append("Net Operating Cash Flow to Net Income")

    if cashOverTMOC < 1:
        flags.append("Cash over 3-Month Operating Costs")
    else:
        ideals.append("Cash over 3-Month Operating Costs")

    if castOverTMOC < 4:
        flags.append("Cash and Short Term Investments over 3-Month Operating Costs")
    else:
        ideals.append("Cash and Short Term Investments over 3-Month Operating Costs")

    print()
    print("The following ratios are worth investigating:")
    for ratio in flags:
        print(ratio)
    print()
    print("The following ratios are ideal:")
    for ratio in ideals:
        print(ratio)

driver()