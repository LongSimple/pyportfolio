import pandas
import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()

class Portfolio:
    def __init__(self, name, portfolioID, stockList):
        self.name = name
        self.portfolioID = portfolioID
        self.stockList = stockList


class Stock:
    def __init__(self, name, ticker):
        self.name = name
        self.ticker = ticker

