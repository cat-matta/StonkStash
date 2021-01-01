#this is to avoid a "module not found" error
#uncomment if you need it

#import sys
#the path below is the location of most of the python libraries on my device
#it will likely work on any other mac but that might not be the case
#sys.path.insert(0, "/usr/local/lib/python3.9/site-packages")

import finnhub

# Setup client
finnhub_client = finnhub.Client(api_key= "bvml27748v6trsjv9u80")

def getStockPrice(companySymbol):
    stockPriceJSON = finnhub_client.quote(companySymbol)
    highPrice = stockPriceJSON['h']
    lowPrice = stockPriceJSON['l']
    print(highPrice)
    print(lowPrice)

#to see the high and low price of a stock with symbol AMZN (for example), use the following line
#getStockPrice('AMZN')
