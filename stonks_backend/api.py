from flask import Flask
from flask import request
from .obtainBalanceSheet import driver
from . import stonkHistoricalData

app = Flask(__name__)

@app.route('/info')
def ratios():
    args = request.args
    symbol = args["symbol"]
    return driver(symbol)

@app.route('/stock')
def prices():
    args = request.args
    symbol, start, interval = args["symbol"], args["start"], args["interval"]
    return stonkHistoricalData.getStockPrices(symbol, start, interval)

@app.route('/MACD')
def getMACD():
    args = request.args
    symbol = args["symbol"]
    return stonkHistoricalData.mostRecentFiftyMACD(symbol)