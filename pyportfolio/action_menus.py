import math

import prompt_toolkit as prompt
from yahoo_fin import stock_info as si


def show_main_menu():
    main_menu_selection = prompt.shortcuts.radiolist_dialog(
        values=[(0, "New Portfolio"), (1, "Existing Portfolio")],
        title="Main Menu",
        text="Please select an option:",
    ).run()
    return main_menu_selection


def select_stock_action(portfolio_list, portfolio_selected, portfolio_stock_choice):
    portfolio_stock_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Show current market capitalization"), (1, "Show the next earnings date"),
                (2, "Show day's trading volume")],
        title="Stock Information",
        text=f"Selected stock is {portfolio_stock_choice} and the current price is ${(round(si.get_live_price(portfolio_stock_choice), 2)):,} please select an action:",
    ).run()
    return portfolio_stock_action


def show_portfolio_action_menu(portfolio_list, portfolio_selected):
    portfolio_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Show Portfolio"), (1, "Manage Portfolio")],
        title=f"{portfolio_list[portfolio_selected].name}",
        text=f"Please select an action:",
    ).run()
    return portfolio_action


def show_portfolio_stock_action_menu(portfolio_stock_action, ticker):
    if portfolio_stock_action == 0:
        result = prompt.shortcuts.button_dialog(
            title="Current Market Capitalization",
            text=f"The current market capitalization of {ticker} is: {get_quote_table_field('Market Cap', ticker)}",
            buttons=[("Okay", "ok")],
        ).run()
    elif portfolio_stock_action == 1:
        result = prompt.shortcuts.button_dialog(
            title="Upcoming Earnings Date",
            text=f"The next earnings date is: {get_quote_table_field('Earnings Date', ticker)}",
            buttons=[("Okay", "ok")],
        ).run()
    elif portfolio_stock_action == 2:
        result = prompt.shortcuts.button_dialog(
            title="Day's Trading Volume",
            text=f"The day's trading volume is: {(math.ceil(get_quote_table_field('Volume', ticker))):,} shares.",
            buttons=[("Okay", "ok")],
        ).run()


def get_quote_table_field(field, ticker):
    quote_table = si.get_quote_table(ticker)
    return quote_table[field]


def show_portfolio_management_action_menu(portfolio_list, portfolio_selected):
    portfolio_management_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Change Portfolio Name"), (1, "Remove Portfolio"), (2, "Remove Equity")],
        title=f"{portfolio_list[portfolio_selected].name}",
        text=f"Please select an action:",
    ).run()
    return portfolio_management_action
