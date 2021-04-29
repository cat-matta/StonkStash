from flask import Flask
from flask import request
from . import obtainBalanceSheet as obs
from . import stonkHistoricalData1 as shd1
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


#returns hourly stock prices over the past 24 hours
@app.route('/stock/day')
def hourlyPricesOverPastDay():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'PT1H', 'P1D')

'''
all of the routes below return daily prices for the stock in
symbol over the period specified in the route
'''
@app.route('/stock/week')
def dailyPricesOverPastWeek():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'P1D', 'P7D')

@app.route('/stock/month')
def dailyPricesOverPastMonth():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'P1D', 'P1M')

@app.route('/stock/quarter')
def dailyPricesOverPastQuarter():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'P1D', 'P3M')

@app.route('/stock/halfyear')
def dailyPricesOverPastHalfYear():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'P1D', 'P6M')

@app.route('/stock/year')
def dailyPricesOverPastYear():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'P1D', 'P1Y')

@app.route('/stock/twoyears')
def dailyPricesOverPastTwoYears():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'P1D', 'P2Y')

@app.route('/stock/fiveyears')
def dailyPricesOverPastFiveYears():
    args = request.args
    symbol = args["symbol"]
    return shd1.getStockPrices(symbol, 'P1D', 'P5Y')
    