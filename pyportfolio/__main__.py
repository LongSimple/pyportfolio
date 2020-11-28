#!/usr/bin/env python
import art
import loaders
import pandas
import prompt_toolkit as prompt
import portfoliotools as ptools

import logging

logging.basicConfig(filename='../log.txt', level=logging.DEBUG)

from yahoo_fin import stock_info as si


def selectPortfolio(portfolio_list):
    portfolio_selected = prompt.shortcuts.radiolist_dialog(
        values=[(x.portfolioID, x.name) for x in portfolio_list],
        title="Portfolio List",
        text="Please select a portfolio:",
    ).run()
    return portfolio_selected


def addStockFlow(stock_list):
    run = 0
    while run == 0:
        stock_name = prompt.shortcuts.input_dialog(
            title="Stock Name", text="Please type the stock name:"
        ).run()
        stock_ticker = prompt.shortcuts.input_dialog(
            title="Stock Ticker", text="Please type the stock ticker in all caps:"
        ).run()
        stock_list.append(ptools.Stock(stock_name, stock_ticker))
        run = prompt.shortcuts.button_dialog(
            title="Add Another Stock",
            text="Would you like to add another stock?",
            buttons=[("Yes", 0), ("No", 1)],
        ).run()
    return stock_list


def newPortfolioFlow(portfolioList):
    portfolio_name = prompt.shortcuts.input_dialog(
        title="Portfolio Name", text="Please type the portfolio name:"
    ).run()
    portfolio_id: int = len(portfolioList)
    stock_list = []
    stock_list = addStockFlow(stock_list)
    portfolioList.append(ptools.Portfolio(portfolio_name, portfolio_id, stock_list))
    return portfolioList


def selectStock(portfolio_list, portfolio_selected):
    portfolio_stock_choice = prompt.shortcuts.radiolist_dialog(
        values=[(x.ticker, x.name) for x in
                [x.stockList for x in portfolio_list if x.portfolioID == portfolio_selected][0]],
        title="Portfolio Overview",
        text="Please select a stock:",
    ).run()
    return portfolio_stock_choice


def selectStockAction(portfolio_list, portfolio_selected, portfolio_stock_choice):
    portfolio_stock_action = prompt.shortcuts.radiolist_dialog(
        values=[(0, "Show current market capitalization"), (1, "Show the next earnings date"),
                (2, "Show analyst ratings")],
        title="Stock Information",
        text=f"Selected stock is {portfolio_stock_choice} and the current price is ${round(si.get_live_price(portfolio_stock_choice), 2)} please select an action:",
    ).run()
    return portfolio_stock_action

def initTestData():
    apple = ptools.Stock("Apple", "AAPL")
    microsoft = ptools.Stock("Microsoft", "MSFT")
    testPortfolio = ptools.Portfolio("Kai Portfolio", 0, [apple, microsoft])
    testPortfolio2 = ptools.Portfolio("Liam Portfolio", 1, [apple])
    portfolio_list = [testPortfolio, testPortfolio2]
    return portfolio_list

def main():
    # print(art.text2art('L33T Portfolio Manager'))
    # fixed_loader = loaders.SpinningLoader(duration = 5)
    # fixed_loader.run()

    # Date based actions:
    #      add profit calculation and percent change calculation
    #      add portfolio tools (date purchased, amount purchased, price)

    # test data
    portfolio_list = initTestData()

    # add database import to portfolio list flow


    main_menu_selection = prompt.shortcuts.radiolist_dialog(
        values=[(0, "New Portfolio"), (1, "Existing Portfolio")],
        title="Main Menu",
        text="Please select an option:",
    ).run()
    if main_menu_selection == 0:
        portfolio_list = newPortfolioFlow(portfolio_list)
        main_menu_selection = 2

    if main_menu_selection == 1:
        portfolio_selected = selectPortfolio(portfolio_list)
        portfolio_action = prompt.shortcuts.radiolist_dialog(
            values=[(0, "Show Portfolio"), (1, "Manage Portfolio")],
            title=f"{portfolio_list[portfolio_selected].name}",
            text=f"Please select an action:",
        ).run()





    # make menu exit on cancel
    # main_menu_selection = 2
    # while main_menu_selection == 2:
    #     main_menu_selection = prompt.shortcuts.radiolist_dialog(
    #         values=[(0, "New Portfolio"), (1, "Existing Portfolio")],
    #         title="Main Menu",
    #         text="Please select an option:",
    #     ).run()
    #     if main_menu_selection == 0:
    #         portfolio_list = newPortfolioFlow(portfolio_list)
    #         main_menu_selection = 2
    #
    #     if main_menu_selection == 1:
    #         portfolio_selected = selectPortfolio(portfolio_list)
    #         portfolio_action = prompt.shortcuts.radiolist_dialog(
    #             values=[(0, "Show Portfolio"), (1, "Manage Portfolio")],
    #             title=f"{portfolio_list[portfolio_selected].name}",
    #             text=f"Please select an action:",
    #         ).run()
    #         if portfolio_action == 0:
    #             portfolio_stock_choice = selectStock(portfolio_list, portfolio_selected)
    #             portfolio_stock_action = selectStockAction(portfolio_list, portfolio_selected, portfolio_stock_choice)
    #             # make these tools work
    #             if portfolio_stock_action == 0:
    #                 result = prompt.shortcuts.button_dialog(
    #                     title="Current Market Capitalization",
    #                     text="The current market capitalization is:",
    #                     buttons=[("Okay", "ok")],
    #                 ).run()
    #             elif portfolio_stock_action == 1:
    #                 result = prompt.shortcuts.button_dialog(
    #                     title="Upcoming Earnings Date",
    #                     text="The next earnings date is:",
    #                     buttons=[("Okay", "ok")],
    #                 ).run()
    #             elif portfolio_stock_action == 2:
    #                 result = prompt.shortcuts.button_dialog(
    #                     title="Analyst Ratings",
    #                     text="The average analyst rating is:",
    #                     buttons=[("Okay", "ok")],
    #                 ).run()
    #             main_menu_selection = 2
    #         if portfolio_action == 1:
    #             portfolio_management_action = prompt.shortcuts.radiolist_dialog(
    #                 values=[(0, "Change Portfolio Name"), (1, "Remove Portfolio"), (2, "Remove Equity")],
    #                 title=f"{portfolio_list[portfolio_selected].name}",
    #                 text=f"Please select an action:",
    #             ).run()
    #             # add portfolio management tools (change portfolio name, remove portfolio, remove equity)
    #             if portfolio_management_action == 0:
    #                 pass
    #             elif portfolio_management_action == 1:
    #                 pass
    #             elif portfolio_management_action == 2:
    #                 pass


# issues with new portfolio flow:
# Requires stock name could automatically draw stock name from ticker
# doesnt check validity of stock name and ticker inputs
# cancel doesnt bring you back to main menu


if __name__ == '__main__':
    main()
