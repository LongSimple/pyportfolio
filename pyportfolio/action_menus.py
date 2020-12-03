from datetime import date as d  # https://docs.python.org/3/library/datetime.html#datetime.date


import math

import prompt_toolkit as prompt
from yahoo_fin import stock_info as si

from pyportfolio.portfolio_utils import get_quote_table_field, select_stock, select_stock_object, index_of_ticker, \
    add_stock_flow


def show_main_menu():
    main_menu_selection = prompt.shortcuts.radiolist_dialog(
        values=[(0, "New Portfolio"), (1, "Existing Portfolio"), (2, "Delete Portfolio")],
        title="Main Menu",
        text="Please select an option:",
    ).run()
    return main_menu_selection


def select_stock_action(portfolio_list, portfolio_selected, portfolio_stock_choice):
    portfolio_stock_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Show current market capitalization"), (1, "Show the next earnings date"),
                (2, "Show day's trading volume"), (3, "Show percent change from purchase date"), (4, "Show quantity owned")],
        title="Stock Information",
        text=f"Selected stock is {portfolio_stock_choice.name} purchased on {portfolio_stock_choice.purchase_date} you own {portfolio_stock_choice.quantity} shares and the current price is ${(round(si.get_live_price(portfolio_stock_choice.stock_ticker), 2)):,} please select an action:",
    ).run()
    return portfolio_stock_action


def show_portfolio_action_menu(portfolio_list, portfolio_selected):
    portfolio_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Show Portfolio"), (1, "Manage Portfolio")],
        title=f"{portfolio_list[portfolio_selected].name}",
        text=f"Please select an action:",
    ).run()
    return portfolio_action


def show_portfolio_stock_action_menu(portfolio_stock_action, stock):
    if portfolio_stock_action == 0:
        result = prompt.shortcuts.button_dialog(
            title="Current Market Capitalization",
            text=f"The current market capitalization of {stock.name} is: {get_quote_table_field('Market Cap', stock.stock_ticker)}",
            buttons=[("Okay", "ok")],
        ).run()
    elif portfolio_stock_action == 1:
        result = prompt.shortcuts.button_dialog(
            title="Upcoming Earnings Date",
            text=f"The next earnings date is: {get_quote_table_field('Earnings Date', stock.stock_ticker)}",
            buttons=[("Okay", "ok")],
        ).run()
    elif portfolio_stock_action == 2:
        result = prompt.shortcuts.button_dialog(
            title="Day's Trading Volume",
            text=f"The day's trading volume is: {(math.ceil(get_quote_table_field('Volume', stock.stock_ticker))):,} shares.",
            buttons=[("Okay", "ok")],
        ).run()
        #percent change from purchase date
    elif portfolio_stock_action == 3:
        purchase_price = stock.data.loc[stock.purchase_date.strftime('%Y-%m-%d'), '4. close']
        current_price = si.get_live_price(stock.stock_ticker)
        percent_change = (purchase_price[0]-current_price)/purchase_price[0]
        result = prompt.shortcuts.button_dialog(
            title="Percent Change from Purchase Date",
            text=f"The percent change from the purchase date is: {round(percent_change, 2)}%.",
            buttons=[("Okay", "ok")],
        ).run()
        #edit quantity owned
    elif portfolio_stock_action == 4:
        result = prompt.shortcuts.button_dialog(
            title="Quantity Owned",
            text=f"You own: {stock.quantity} shares.",
            buttons=[("Okay", "ok")],
        ).run()


def show_portfolio_management_action_menu(portfolio_list, portfolio_selected):
    portfolio_management_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Change Portfolio Name"), (1, "Remove Equity"), (2, "Add Equity")],
        title=f"{portfolio_list[portfolio_selected].name}",
        text=f"Please select an action:",
    ).run()
    return portfolio_management_action


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
    #might add change quantity owned


def change_portfolio_name(portfolio_list, portfolio_selected):
    portfolio_list[portfolio_selected].name = prompt.shortcuts.input_dialog(
        title="Portfolio Name", text="Please type a new portfolio name:"
    ).run()


def select_portfolio(portfolio_list):
    portfolio_selected = prompt.shortcuts.radiolist_dialog(
        values=[(x.portfolio_id, x.name) for x in portfolio_list],
        title="Portfolio List",
        text="Please select a portfolio:",
    ).run()
    return portfolio_selected