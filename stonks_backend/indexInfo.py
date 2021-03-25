import urllib.request
import bs4 as bs
import re

def getTextFromTdElements(stonksoup):
    tdList = []
    for stocklabel in stonksoup.find_all('td'):
        text = stocklabel.string
        if text:
            tdList.append(text)
    return tdList

def getTextFromBgQuoteElements(stonksoup):
    bgQuoteList = []
    for quote in stonksoup.find_all('bg-quote'):
        text = quote.string
        if text:
            bgQuoteList.append(text)
    return bgQuoteList

def setupIndexDict(tdList, bgQuoteList):
    info = {}

    verifyDateAndTime = re.compile("([a-zA-Z]{3}) (\d{1,2}), (\d{4}) (\d{1,2}):(\d{2}) ([ap]{1})\.m\. ")

    for i in range(len(bgQuoteList)):
        if verifyDateAndTime.fullmatch(bgQuoteList[i]):
            info["Index"] = bgQuoteList[i+1]
            info["Daily Change"] = bgQuoteList[i+2]
            info["Daily Percent Change"] = bgQuoteList[i+3]
            break

    for i in range(len(tdList)):
        if tdList[i] == "5 Day":
            info["Previous Close"] = tdList[i-1]
        if tdList[i] == "IPC Indice de Precios Y Cotizaciones":
            start = i+4
            break

    counter = 0
    info["Components"] = {}
    for i in range(start,len(tdList)):
        if counter == 0:
            header = tdList[i]
            info["Components"][header] = {}
        if counter == 1:
            info["Components"][header]["Last"] = tdList[i]
        if counter == 2:
            info["Components"][header]["Change"] = tdList[i]
        if counter == 3:
            info["Components"][header]["Change%"] = tdList[i]
        counter += 1
        if counter == 4:
            counter = 0

    return info

def getIndexInfo(index):
    opener = urllib.request.urlopen('https://www.marketwatch.com/investing/index/' + index).read()
    stonksoup = bs.BeautifulSoup(opener,'lxml')

    #the previous close and all info on the stocks making up the index
    #are enclosed in td tags, so tdList now contains all text enclosed
    #in a td tag
    tdList = getTextFromTdElements(stonksoup)

    #what the index is currently at, the daily change, and the percent
    #daily change are all enclosed in bg-quote tags, so bgQuoteList now
    #contains all text enclosed in a bg-quote tag
    bgQuoteList = getTextFromBgQuoteElements(stonksoup)

    #using the above two lists, sets up the dictionary containing the index's info
    info = setupIndexDict(tdList,bgQuoteList)
    return info


#return: dict containing info on the Dow Jones, S&P, Nasdaq
def driver():
    #djia is dow jones, spx is s&p 500, comp is nasdaq
    dowInfo = getIndexInfo('djia')
    sANDpInfo = getIndexInfo('spx')
    nasdaqInfo = getIndexInfo('comp')
    bigThreeIndices = {"Dow Jones": dowInfo, "S&P 500": sANDpInfo, "Nasdaq": nasdaqInfo}
    return bigThreeIndices

print(driver())
