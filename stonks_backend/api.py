from flask import Flask
from finder import driver

app = Flask(__name__)

@app.route('/info')
driver()