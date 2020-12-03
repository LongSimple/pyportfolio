from datetime import date as d  #https://docs.python.org/3/library/datetime.html#datetime.date
import prompt_toolkit as prompt #https://python-prompt-toolkit.readthedocs.io/en/master/


class Portfolio:
    def __init__(self, name, portfolio_id, stock_list):
        self.name = name
        self.portfolio_id = portfolio_id
        self.stock_list = stock_list


class Stock:
    def __init__(self, name, ticker, amount_purchased, purchase_date=d.today):
        self.name = name
        self.ticker = ticker
        self.purchase_date = purchase_date
        self.amount_purchased = amount_purchased


def select_portfolio(portfolio_list):
    portfolio_selected = prompt.shortcuts.radiolist_dialog(
        values=[(x.portfolio_id, x.name) for x in portfolio_list],
        title="Portfolio List",
        text="Please select a portfolio:",
    ).run()
    return portfolio_selected


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
                title="Stock Purchase Date", text="Please type the date you purchased the stock in the form (DD,MM,YYYY):"
            ).run()
        year, month, day = map(int, stock_date.split(','))
        stock_date = d(day, month, year)
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
        values=[(x.ticker, x.name) for x in
                [x.stock_list for x in portfolio_list if x.portfolio_id == portfolio_selected][0]],
        title="Portfolio Overview",
        text="Please select a stock:",
    ).run()
    return portfolio_stock_choice


# could make this a set of different functions
def remove_portfolio(portfolio_list):
    index = index_of_portfolio_id(portfolio_list, select_portfolio(portfolio_list))
    portfolio_list.pop(index)

def portfolio_management_tools(portfolio_management_action, portfolio_list, portfolio_selected):
    # change portfolio name
    if portfolio_management_action == 0:
        change_portfolio_name(portfolio_list, portfolio_selected)
    # remove equity
    elif portfolio_management_action == 1:
        stock_selected = select_stock(portfolio_list, portfolio_selected)
        index_of_stock_selected = index_of_ticker(portfolio_list[portfolio_selected].stock_list, stock_selected)
        portfolio_list[portfolio_selected].stock_list.pop(index_of_stock_selected)
    #add equity
    elif portfolio_management_action == 2:
        portfolio_list[portfolio_selected].stock_list = add_stock_flow(portfolio_list[portfolio_selected].stock_list)

def index_of_ticker(l, name):
    for i in range(len(l)):
        if l[i].ticker == name:
            return i
    return -1

def index_of_portfolio_id(l, name):
    for i in range(len(l)):
        if l[i].portfolio_id == name:
            return i
    return -1

def change_portfolio_name(portfolio_list, portfolio_selected):
    portfolio_list[portfolio_selected].name = prompt.shortcuts.input_dialog(
        title="Portfolio Name", text="Please type a new portfolio name:"
    ).run()
