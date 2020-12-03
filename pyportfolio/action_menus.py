import math

import prompt_toolkit as prompt
from yahoo_fin import stock_info as si


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
                (2, "Show day's trading volume")],
        title="Stock Information",
        text=f"Selected stock is {portfolio_stock_choice.name} purchased on {portfolio_stock_choice.purchase_date} you own {portfolio_stock_choice.amount_purchased} shares and the current price is ${(round(si.get_live_price(portfolio_stock_choice.ticker), 2)):,} please select an action:",
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
            text=f"The current market capitalization of {stock.name} is: {get_quote_table_field('Market Cap', stock.ticker)}",
            buttons=[("Okay", "ok")],
        ).run()
    elif portfolio_stock_action == 1:
        result = prompt.shortcuts.button_dialog(
            title="Upcoming Earnings Date",
            text=f"The next earnings date is: {get_quote_table_field('Earnings Date', stock.ticker)}",
            buttons=[("Okay", "ok")],
        ).run()
    elif portfolio_stock_action == 2:
        result = prompt.shortcuts.button_dialog(
            title="Day's Trading Volume",
            text=f"The day's trading volume is: {(math.ceil(get_quote_table_field('Volume', stock.ticker))):,} shares.",
            buttons=[("Okay", "ok")],
        ).run()
        #percent change from purchase date
    elif portfolio_stock_action == 3:
        pass
        #edit quantity owned
    elif portfolio_stock_action == 4:
        pass


def get_quote_table_field(field, ticker):
    quote_table = si.get_quote_table(ticker)
    return quote_table[field]


def show_portfolio_management_action_menu(portfolio_list, portfolio_selected):
    portfolio_management_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Change Portfolio Name"), (1, "Remove Equity"), (2, "Add Equity")],
        title=f"{portfolio_list[portfolio_selected].name}",
        text=f"Please select an action:",
    ).run()
    return portfolio_management_action
