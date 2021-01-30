import pandas as pd
import urllib as urlpull
import urllib.request
import bs4 as bs

#put the stock symbol you want here
stockSymbol = 'AAPL'
datastuff = 'https://finance.yahoo.com/quote/' + stockSymbol + '/balance-sheet/' ##basically the link, we need to find a way to inject the stock name into the link


opener = urllib.request.urlopen(datastuff).read() ##opens the html page
stonksoup = bs.BeautifulSoup(opener,'lxml') ##turns it to xml format

balancelist = [] ##create a list to add anything with the span tag
for stockdata in stonksoup.find_all('span'): ##finds all the span tags
    balancelist.append(stockdata.string)##filters out span and gives only the string value related to the span

flag = 0
for i in range(len(balancelist)):
    if balancelist[i] == "Breakdown":
        start = i
        flag = 1
    if balancelist[i] == "Learn more" and flag == 1:
        end = i
        break

counter = 0
i = start
while balancelist[i] != "Total Assets":
    i = i + 1
    counter = counter + 1

breakdown = {}
counter2 = 0
for i in range(start+counter, end):
    if counter2 == 0:
        currentHeading = balancelist[i]
        breakdown[currentHeading] = {}
    else:
        breakdown[currentHeading][balancelist[start+counter2]] = balancelist[i]
    counter2 = counter2+1
    if counter2 == counter:
        counter2 = 0

#breakdown has dictionary of all stock data contained in the url in the variable datastuff
#uncomment the next line to see the dictionary
#print(breakdown)
