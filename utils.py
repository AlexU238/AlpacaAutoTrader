#-------------------------------------------------------------------------------------------
# Name:        utils
# Purpose:     contains helper functions
#
# Author:      U238 (https://github.com/AlexU238)
#
# Last Edit:   07/09/2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#-------------------------------------------------------------------------------------------

from dataclasses import dataclass

#StockUseData is used to keep track of stocks amount to be bought/sold
@dataclass
class StockUseData:
    symbol: str
    amount: int
    price: float


#function returns how much money will be spent per position
def get_usable_balance_per_stock(total_usable_balance, stock_list):
    #total_usable_balance - total balance that you are willing to spend on stocks
    #total_usable_balance: float
    #stock_list - list of symbols of stocks
    #stock_list: list of strings
    return int(total_usable_balance/len(stock_list))

#function returns the amount of stocks that can be bought for the entered balance
def get_amount_of_stocks_to_buy(stock_price, usable_balance):
    #stock_price - price of a needed stock
    #stock_price: float
    #usable_balance - how much you are willing to spend on this stock
    #usable_balance: float
    return int(usable_balance/stock_price)

#function returns a list of StockUseData with all amounts set to zero
def create_stock_use_data_list(symbols):
    #symbols - list of stock symbols
    #symbols: list of strings
    stock_use_data_list = []
    for symbol in symbols:
        stock_use_data_list.append(StockUseData(symbol=symbol, amount=0, price=0))
    return stock_use_data_list
