import pandas as pd
import urllib as urlpull
import urllib.request
import bs4 as bs
import re

stockSymbol = 'gme'
datastuff = 'https://www.marketwatch.com/investing/stock/' + stockSymbol+ '/financials/balance-sheet/quarter' ##basically the link, we need to find a way to inject the stock name into the link


opener = urllib.request.urlopen(datastuff).read() ##opens the html page
stonksoup = bs.BeautifulSoup(opener,'lxml') ##turns it to xml format

verifyDate = re.compile("(\d{2})-([a-zA-Z]{3})-(\d{4})")

flag = 0
balancelist = [] ##create a list to add anything with the div tag
for stocklabel in stonksoup.find_all('div'):
    balancelist.append(stocklabel.string)

for i in range(len(balancelist)):
    if balancelist[i] == "Item":
        if verifyDate.fullmatch(balancelist[i+1]):
            startAssets = i+1

    if balancelist[i] == "Total Assets Growth":
        endAssets = i+7
        break

for i in range(endAssets, len(balancelist)):
    if balancelist[i] == "Item":
        if verifyDate.fullmatch(balancelist[i+1]):
            startLiabilities = i+1

    if balancelist[i] == "Liabilities & Shareholders' Equity":
        endLiabilities = i+7
        break

#startAssets is the index where the first of the five quarters are in the Assets table in balancelist
#startLiabilites is the index where the first of the five quarters are in the Liabilities table in balancelist

assets = {}
counter1 = 0
counter2 = -1
for i in range(startAssets+6, endAssets):

    if counter1 == 0:
        heading = balancelist[i]
        assets[heading] = {}

    if counter1 == 2:
        counter2 = 0

    if counter2 == 5:
        counter2 = -1

    if counter2 != -1:
        assets[heading][balancelist[startAssets+counter2]] = balancelist[i]
        counter2 = counter2 + 1

    counter1 = counter1 + 1
    if counter1 == 10:
        counter1 = 0

#assets is a dictionary which has all of the information in the Assets table

liabilities = {}
counter1 = 0
counter2 = -1
for i in range(startLiabilities+6, endLiabilities):

    if counter1 == 0:
        heading = balancelist[i]
        liabilities[heading] = {}

    if counter1 == 2:
        counter2 = 0

    if counter2 == 5:
        counter2 = -1

    if counter2 != -1:
        liabilities[heading][balancelist[startLiabilities+counter2]] = balancelist[i]
        counter2 = counter2 + 1

    counter1 = counter1 + 1
    if counter1 == 10:
        counter1 = 0

#liabilities is a dictionary which has all of the information in the Liabilities table