from flask import Flask
from .finder import driver

app = Flask(__name__)

@app.route('/info')
def main():
    stonks = dict()
    stonks = driver()
    return stonks