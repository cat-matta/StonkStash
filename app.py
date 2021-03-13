#from stonks_backend.main import *
#from stonks_backend.sciencestuff import *
from stonks_server.server import server
from stonks_server.auth import auth

from flask import Flask, render_template, current_app, send_from_directory
import os

#stock_name="TSLA"
#stock_date="2021-01-21"
#plotname=driver(stock_name,stock_date)
#filename=graph_stuff()
#print(plotname)
app = Flask(__name__)
# app.config['stock_name']=stock_name
# app.config['stock_date']=stock_date
# app.config['plotname']=plotname
app.config['DOWNLOADS'] = "stonks_server/downloads"

app.register_blueprint(server,url_prefix="")
app.register_blueprint(auth,url_prefix="")

@app.route('/display')
def display():
    return render_template("display.html",stock_name=stock_name,stock_date=stock_date,plotname=plotname)



if __name__ == '__main__':
    app.run(debug=True)


