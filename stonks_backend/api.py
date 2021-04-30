from flask import Flask
from flask import request
from . import obtainBalanceSheet as obs
from . import stonkHistoricalData as shd
from . import indexInfo as ii
import time
import ciso8601

app = Flask(__name__)

#this route returns balance sheet info for the stock in symbol
@app.route('/info')
def ratios():
    args = request.args
    symbol = args["symbol"]
    return obs.driver(symbol)

#this route returns info from the three major stock market indices
#dow jones, nasdaq, and s&p 500
@app.route('/index')
def threeBigIndices():
    return ii.driver()

'''
this route returns the stock prices of the stock in symbol
in the period starting at start and ending in end. start
and end are unix timestamps. Interval is how spaced out
consecutive prices are, and can be one of H, D, W, or M.
'''
@app.route('/stock')
def prices():
    args = request.args
    symbol, start, end, interval = args["symbol"], args["start"], args["end"], args["interval"]
    return shd.getStockPrices(symbol, int(float(start)), int(float(end)), interval)

'''
returns hourly stock prices over the past 24 hours
'''
@app.route('/stock/day')
def hourlyPricesOverPastDay():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 86_400
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'H')

'''
all of the routes below return daily prices for the stock in
symbol over the period specified in the route
'''
@app.route('/stock/week')
def dailyPricesOverPastWeek():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 604_800 #seconds in 7 days
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'D')

@app.route('/stock/month')
def dailyPricesOverPastMonth():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 2_678_400 #seconds in 31 days
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'D')

@app.route('/stock/quarter')
def dailyPricesOverPastQuarter():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 7_862_400 #seconds in 91 days
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'D')

@app.route('/stock/halfyear')
def dailyPricesOverPastHalfYear():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 15_724_800 #seconds in 182 days
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'D')

@app.route('/stock/year')
def dailyPricesOverPastYear():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 31_536_000 #seconds in 365 days
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'D')

@app.route('/stock/twoyears')
def dailyPricesOverPastTwoYears():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 63_072_000 #seconds in 730 days
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'D')

@app.route('/stock/fiveyears')
def dailyPricesOverPastFiveYears():
    args = request.args
    symbol = args["symbol"]
    endUnixTime = int( time.time() )
    startUnixTime = endUnixTime - 157_766_400 #seconds in 1826 days
    return shd.getStockPrices(symbol, startUnixTime, endUnixTime, 'D')
    