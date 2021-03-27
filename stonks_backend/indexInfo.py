import urllib.request
import bs4 as bs
import re

#################################################
#################################################
##                                             ##
##  the driver function is the magic, the rest ##
##  are methods which are called by it         ##
##                                             ##
#################################################
#################################################

#param: stonksoup is the result of hitting a webpage with Beautiful Soup
#       in particular, it's the "soup" of the page containing the desired
#       index's information
#
#return: list with all strings enclosed in td tags
def getTextFromTdElements(stonksoup):
    tdList = []
    for stocklabel in stonksoup.find_all('td'):
        text = stocklabel.string
        if text:
            tdList.append(text)
    return tdList


#param: stonksoup is the result of hitting a webpage with Beautiful Soup
#       in particular, it's the "soup" of the page containing the desired
#       index's information
#
#return: list with all strings enclosed in bg-quote tags
def getTextFromBgQuoteElements(stonksoup):
    bgQuoteList = []
    for quote in stonksoup.find_all('bg-quote'):
        text = quote.string
        if text:
            bgQuoteList.append(text)
    return bgQuoteList


#param: tdList is the list of all text enclosed in td tags
#       bgQuoteList is the list of all text enclosed in bg-quote tags
#
#return: dict with all of the info on a particular index
def setupIndexDict(tdList, bgQuoteList):
    info = {}

    #regex matching a string with a date and time
    #the index price, daily change, and percent daily change are always
    #a predictable number of lines away from a line matching this regex
    verifyDateAndTime = re.compile("([a-zA-Z]{3}) (\d{1,2}), (\d{4}) (\d{1,2}):(\d{2}) ([ap]{1})\.m\. ")

    #once I find the line matching the above regex, I know where the index price,
    #daily change, and percent daily change are
    for i in range(len(bgQuoteList)):
        if verifyDateAndTime.fullmatch(bgQuoteList[i]):
            info["Index"] = bgQuoteList[i+1]
            info["Daily Change"] = bgQuoteList[i+2]
            info["Daily Percent Change"] = bgQuoteList[i+3]
            break


    for i in range(len(tdList)):
        #the previous close is always at the line before it says "5 Day"
        if tdList[i] == "5 Day":
            info["Previous Close"] = tdList[i-1]

        #four lines after the below string is where all of the components
        #of the index are, so I set the start variable and use that as the
        #start of the next for loop
        if tdList[i] == "IPC Indice de Precios Y Cotizaciones":
            start = i+4
            break


    #this for loop gets all of the info on the components of the index
    #each stock has three pieces of information, so every four lines is
    #a new stock (three pieces of info+stock name gives you four lines)
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


#param: index is a string containing market watch's code for the index
#       it's always one of djia, comp, or spx
#
#return: dict containing info on the index indicated by the parameter
def getIndexInfo(index):

    #opens up the page with the desired index's information
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



#this is the function that will be called in the api
#return: dict containing info on the Dow Jones, S&P, Nasdaq
def driver():

    #djia is dow jones, spx is s&p 500, comp is nasdaq

    #puts dict with dow jones info in dowInfo
    dowInfo = getIndexInfo('djia')

    #puts dict with S&P info in sANDpInfo
    sANDpInfo = getIndexInfo('spx')

    #puts dict with nasdaq info in nasdaqInfo
    nasdaqInfo = getIndexInfo('comp')

    #packages the above three dicts in a single dict
    bigThreeIndices = {"Dow Jones": dowInfo, "S&P 500": sANDpInfo, "Nasdaq": nasdaqInfo}
    return bigThreeIndices

