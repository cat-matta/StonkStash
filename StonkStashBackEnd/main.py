import finnhub
import time
import datetime as dt
import os
from dotenv import load_dotenv # for the API key

load_dotenv() # hiding our API key
TOKEN = os.environ.get("token")

#week is 7 days
#month is 30 days
#quarter is 91 days
#semiannual is 182 days
#year is 365 days
periods = {"w": 604800, "m": 2592000, "q": 2592000, "s": 15724800, "y": 31536000}
# Setup client
finnhub_client = finnhub.Client(api_key= TOKEN)

def getStockPrice(companySymbol):
    stockPriceJSON = finnhub_client.quote(companySymbol)
    highPrice = stockPriceJSON['h']
    lowPrice = stockPriceJSON['l']
    return highPrice, lowPrice

def getStockCandles(companySymbol,resolution,end,period):
    end = int(time.mktime(dt.datetime.strptime(end, "%Y-%m-%d").timetuple()))
    start = end - periods[period]
    candles = finnhub_client.stock_candles(companySymbol,resolution,start,end)
    return candles
    
def getStockCandlesToday(companySymbol):
    end = int(time.time())
    start = end - periods["m"]
    candles = finnhub_client.stock_candles(companySymbol,'D',start,end)
    return candles

#to see the high and low price of a stock with symbol AMZN (for example), use the following line
#getStockPrice('AMZN')
