from flask import Flask
from flask import request
from .obtainBalanceSheet import driver
from .main import *

app = Flask(__name__)

@app.route('/info')
def ratios():
    args = request.args
    symbol = args["symbol"]
    return driver(symbol)

@app.route('/stock')
def candles():
    args = request.args
    symbol, res, end, period = args["symbol"], args["res"], args["end"], args["period"]
    return getStockCandles(symbol, res, end, period)