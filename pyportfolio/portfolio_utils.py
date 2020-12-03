from datetime import date as d  # https://docs.python.org/3/library/datetime.html#datetime.date
import prompt_toolkit as prompt  # https://python-prompt-toolkit.readthedocs.io/en/master/
# api_key=H5BDQ0DGNCED6EAU
from alpha_vantage.timeseries import TimeSeries
# add unique portfolio id to make indexing better
from yahoo_fin import stock_info as si

import pyportfolio.action_menus as am

ts = TimeSeries(key='H5BDQ0DGNCED6EAU', output_format='pandas')


class Portfolio:
    def __init__(self, name, portfolio_id, stock_list):
        self.name = name
        self.portfolio_id = portfolio_id
        self.stock_list = stock_list


# add unique stock_id to make indexing better
class Stock:
    def __init__(self, name, stock_ticker, quantity, purchase_date, stock_id=0):
        self.name = name
        self.stock_ticker = stock_ticker
        self.purchase_date = purchase_date
        self.quantity = quantity
        self.stock_id = stock_id
        data, meta_data = ts.get_daily(symbol=stock_ticker, outputsize='full')
        self.data = data
        self.meta_data = meta_data

    def update_data(self):
        data, meta_data = ts.get_daily(symbol=self.stock_ticker, outputsize='full')
        self.data = data
        self.meta_data = meta_data


def add_stock_flow(stock_list):
    run = 0
    while run == 0:
        stock_name = None
        stock_ticker = None
        stock_date = None
        stock_quantity = None
        while stock_name is None:
            stock_name = prompt.shortcuts.input_dialog(
                title="Stock Name", text="Please type the stock name:"
            ).run()
        while stock_ticker is None:
            stock_ticker = prompt.shortcuts.input_dialog(
                title="Stock Ticker", text="Please type the stock ticker in all caps:"
            ).run()
        while stock_date is None:
            stock_date = prompt.shortcuts.input_dialog(
                title="Stock Purchase Date",
                text="Please type the date you purchased the stock in the form (YYYY,MM,DD) weekends do not work:"
            ).run()
        year, month, day = map(int, stock_date.split(','))
        stock_date = d(year, month, day)
        while stock_quantity is None:
            stock_quantity = prompt.shortcuts.input_dialog(
                title="Stock Quantity Purchased", text="Please type the quantity of the stock you purchased:"
            ).run()
        stock_list.append(Stock(stock_name, stock_ticker, stock_quantity, stock_date))
        run = prompt.shortcuts.button_dialog(
            title="Add Another Stock",
            text="Would you like to add another stock?",
            buttons=[("Yes", 0), ("No", 1)],
        ).run()
    return stock_list


def new_portfolio_flow(portfolio_list):
    while True:
        portfolio_name = prompt.shortcuts.input_dialog(
            title="Portfolio Name", text="Please type the portfolio name:"
        ).run()
        if portfolio_name is not None:
            portfolio_id: int = len(portfolio_list)
            stock_list = []
            stock_list = add_stock_flow(stock_list)
            portfolio_list.append(Portfolio(portfolio_name, portfolio_id, stock_list))
            return portfolio_list
        if portfolio_name is None:
            return None


def select_stock(portfolio_list, portfolio_selected):
    portfolio_stock_choice = prompt.shortcuts.radiolist_dialog(
        values=[(x.stock_ticker, x.name) for x in
                [x.stock_list for x in portfolio_list if x.portfolio_id == portfolio_selected][0]],
        title="Portfolio Overview",
        text="Please select a stock:",
    ).run()
    return portfolio_stock_choice


def select_stock_object(portfolio_list, portfolio_selected):
    portfolio_stock_choice = prompt.shortcuts.radiolist_dialog(
        values=[(x, x.name) for x in
                [x.stock_list for x in portfolio_list if x.portfolio_id == portfolio_selected][0]],
        title="Portfolio Overview",
        text="Please select a stock:",
    ).run()
    return portfolio_stock_choice


# could make this a set of different functions
def remove_portfolio(portfolio_list):
    index = index_of_portfolio_id(portfolio_list, am.select_portfolio(portfolio_list))
    portfolio_list.pop(index)


def index_of_ticker(l, name):
    for i in range(len(l)):
        if l[i].stock_ticker == name:
            return i
    return -1


def index_of_portfolio_id(l, name):
    for i in range(len(l)):
        if l[i].portfolio_id == name:
            return i
    return -1


def get_quote_table_field(field, stock_ticker):
    quote_table = si.get_quote_table(stock_ticker)
    return quote_table[field]
