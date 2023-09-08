#---------------------------------------------------------------------------------
# Name:        orders
# Purpose:     contains functions/requests for ask, bid, and last trade stock prices
#
# Author:      U238 (https://github.com/AlexU238)
#
# Last Edit:   23/08/2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#---------------------------------------------------------------------------------

from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockLatestTradeRequest
from alpaca.common.exceptions import APIError
import json

#function returns latest ask price for single stock/symbol
def get_current_ask_price(data_client,stock):
    #data_client - alpaca client to see historical data
    #data_client: StockHistoricalDataClient
    #stock - stock symbol
    #stock: string
    request_params = StockLatestQuoteRequest(symbol_or_symbols=stock)
    try:
        latest_quote = data_client.get_stock_latest_quote(request_params)
    except APIError as error:
        print(f"Error in requesting ask price: {error.status_code} - ", json.loads(str(error))["message"])
        return -1
    return latest_quote[stock].ask_price

#function returns latest ask price for single stock/symbol
def get_current_bid_price(data_client,stock):
    #data_client - alpaca client to see historical data
    #data_client: StockHistoricalDataClient
    #stock - stock symbol
    #stock: string
    request_params = StockLatestQuoteRequest(symbol_or_symbols=stock)
    try:
        latest_quote = data_client.get_stock_latest_quote(request_params)
    except APIError as error:
        print(f"Error in requesting bid price: {error.status_code} - ", json.loads(str(error))["message"])
        return -1
    return latest_quote[stock].bid_price

#function returns latest ask price for single stock/symbol
def get_current_trade_price(data_client,stock):
    #data_client - alpaca client to see historical data
    #data_client: StockHistoricalDataClient
    #stock - stock symbol
    #stock: string
    request_params = StockLatestTradeRequest(symbol_or_symbols=stock)
    try:
        latest_quote = data_client.get_stock_latest_trade(request_params)
    except APIError as error:
        print(f"Error in requesting last trade price: {error.status_code} -", json.loads(str(error))["message"])
        return -1
    return latest_quote[stock].price
