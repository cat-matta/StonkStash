import pandas as pd
import urllib as urlpull
import urllib.request
import bs4 as bs
datastuff = 'https://www.marketwatch.com/investing/stock/tsla/financials/balance-sheet/quarter' ##basically the link, we need to find a way to inject the stock name into the link


opener = urllib.request.urlopen(datastuff).read() ##opens the html page
stonksoup = bs.BeautifulSoup(opener,'lxml') ##turns it to xml format
##print(stonksoup.title)
balancelist = [] ##create a list to add anything with the span tag
for stockdata in stonksoup.find_all('span'): ##finds all the span tags
    balancelist.append(stockdata.string)##filters out span and gives only the string value related to the span
labelthestock = []
for stocklabel in stonksoup.find_all('div'):
    if(stocklabel.string != None and stocklabel.string != "_"):
        print(stocklabel.string)

'''
for i in range(len(balancelist)):
    print(i,balancelist[i])


for i in range(len(labelthestock)):
    print(i,labelthestock[i])

'''