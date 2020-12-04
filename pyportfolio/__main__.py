#!/usr/bin/env python
import os.path
import pickle  # https://docs.python.org/3/library/pickle.html

import pyportfolio.action_menus as menu
from pyportfolio.portfolio_utils import new_portfolio_flow, remove_portfolio, select_stock_object


# refactor
def main(loaded_portfolios):
    """
    Main menu program that shows a set of portfolio tools.
    :param loaded_portfolios: list of portfolio objects.
    """
    while True:
        main_menu_selection = menu.show_main_menu()
        if main_menu_selection is None:
            # exit program
            save_data(loaded_portfolios)
            exit()
        if main_menu_selection == 0:
            # add new portfolio
            loaded_portfolios = new_portfolio_flow(loaded_portfolios)
            save_data(loaded_portfolios)
        if main_menu_selection == 1:
            # show portfolio menus
            while True:
                # select portfolio object to work with
                portfolio_selected = menu.select_portfolio(loaded_portfolios)
                if portfolio_selected is None:
                    save_data(loaded_portfolios)
                    break
                while True:
                    # select an action to do with selected portfolio (could refactor to use portfolio selected index or id).
                    portfolio_action = menu.show_portfolio_action_menu(loaded_portfolios, portfolio_selected)
                    if portfolio_action is None:
                        save_data(loaded_portfolios)
                        break
                    elif portfolio_action == 0:
                        while True:
                            # select a stock to do an action on.
                            portfolio_stock_choice = select_stock_object(loaded_portfolios, portfolio_selected)
                            if portfolio_stock_choice is None:
                                break
                            while True:
                                # select an action to do on a stock.
                                portfolio_stock_action = menu.select_stock_action(portfolio_stock_choice)
                                if portfolio_stock_action is None:
                                    save_data(loaded_portfolios)
                                    break
                                while True:
                                    # do selected action on stock
                                    menu.show_portfolio_stock_actions(portfolio_stock_action, portfolio_stock_choice)
                                    save_data(loaded_portfolios)
                                    break


                    elif portfolio_action == 1:
                        # portfolio management tools flow
                        portfolio_management_action = menu.show_portfolio_management_actions(loaded_portfolios,
                                                                                             portfolio_selected)
                        loaded_portfolios = menu.portfolio_management_tools(portfolio_management_action,
                                                                            loaded_portfolios, portfolio_selected)
                        save_data(loaded_portfolios)
        if main_menu_selection == 2:
            # remove portfolio from the portfolio database.
            remove_portfolio(loaded_portfolios)
            save_data(loaded_portfolios)


def load_data(path="portfolio_list.pkl"):
    """
    This function checks if there is an existing database and loads that database. If there is no database it creates one.
    :param: path: path to file containing the database.
    :return:portfolio_list: list of portfolios and their associated data.
    """
    file_exists = os.path.isfile(path)
    if file_exists:
        portfolio_load = pickle.load(open(path, "rb"))
        return portfolio_load
    else:
        portfolio_load = []
        portfolio_load = new_portfolio_flow(portfolio_load)
        pickle.dump(portfolio_load, open(path, "wb"))
        return portfolio_load


def save_data(portfolio_dump, path="portfolio_list.pkl"):
    """
    This function saves the portfolio_list to a database as a .pkl file.
    :param portfolio_dump: portfolio_list to be saved to database.
    :param path: path to file containing the database.
    """
    pickle.dump(portfolio_dump, open(path, "wb"))


if __name__ == '__main__':
    portfolio_list = load_data()
    save_data(portfolio_list)
    main(portfolio_list)
