#!/usr/bin/env python
import logging
import pickle
import os.path

from pyportfolio.action_menus import show_main_menu, select_stock_action, show_portfolio_action_menu, \
    show_portfolio_stock_action_menu, show_portfolio_management_action_menu
from pyportfolio.portfolio_utils import select_portfolio, new_portfolio_flow, select_stock, Portfolio, Stock, \
    portfolio_management_tools, remove_portfolio

def initTestData():
    apple = Stock("Apple", "AAPL")
    microsoft = Stock("Microsoft", "MSFT")
    test_portfolio = Portfolio("Kai Portfolio", 0, [apple, microsoft])
    test_portfolio2 = Portfolio("Liam Portfolio", 1, [apple])
    portfolio_list = [test_portfolio, test_portfolio2]
    return portfolio_list


def main(first_run, portfolio_list):
    if first_run == 1:
        pickle.dump(portfolio_list, open("portfolio_list.pkl", "wb"))
    pickle.dump(portfolio_list, open("portfolio_list.pkl", "wb"))
    while True:
        main_menu_selection = show_main_menu()
        if main_menu_selection is None:
            pickle.dump(portfolio_list, open("portfolio_list.pkl", "wb"))
            exit()
        if main_menu_selection == 0:
            portfolio_list2 = new_portfolio_flow(portfolio_list)
            if portfolio_list2 is None:
                portfolio_list = portfolio_list
            else:
                portfolio_list = portfolio_list2
        if main_menu_selection == 1:
            while True:
                portfolio_selected = select_portfolio(portfolio_list)
                if portfolio_selected is None:
                    break
                while True:
                    portfolio_action = show_portfolio_action_menu(portfolio_list, portfolio_selected)
                    if portfolio_action is None:
                        break
                    if portfolio_action == 0:
                        while True:
                            portfolio_stock_choice = select_stock(portfolio_list, portfolio_selected)
                            if portfolio_stock_choice is None:
                                break
                            while True:
                                portfolio_stock_action = select_stock_action(portfolio_list, portfolio_selected,
                                                                             portfolio_stock_choice)
                                if portfolio_stock_action is None:
                                    break
                                while True:
                                    result = show_portfolio_stock_action_menu(portfolio_stock_action, portfolio_stock_choice)
                                    if result is None:
                                        break
                    elif portfolio_action == 1:
                        portfolio_management_action = show_portfolio_management_action_menu(portfolio_list,
                                                                                            portfolio_selected)
                        portfolio_management_tools(portfolio_management_action, portfolio_list, portfolio_selected)
        if main_menu_selection == 2:
            remove_portfolio(portfolio_list)

if __name__ == '__main__':
    file_exists = os.path.isfile("portfolio_list.pkl")
    if file_exists:
        first_run = 0
        portfolio_list = pickle.load(open("portfolio_list.pkl", "rb"))
        main(first_run, portfolio_list)
    else:
        first_run = 1
        f = open("portfolio_list.pkl", "w")
        portfolio_list = []
        portfolio_list = new_portfolio_flow(portfolio_list)
        main(first_run, portfolio_list)