#-------------------------------------------------------------------------------
# Name:        orders
# Purpose:     contains the order function for communication with API
#
# Author:      U238 (https://github.com/AlexU238)
#
# Last Edit:   23/08/2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#-------------------------------------------------------------------------------

from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.requests import MarketOrderRequest
from alpaca.common.exceptions import APIError
import sys
import json


def market_order(stock_symbol,quantity,client,order_side):
    market_order_data=MarketOrderRequest(
    symbol=stock_symbol,
    qty=quantity,
    side=order_side,
    time_in_force=TimeInForce.GTC
    )
    market_order = client.submit_order(market_order_data)




def marker_buy_order(stock_symbol,quantity, client):
    try:
        market_order(stock_symbol,quantity,client,OrderSide.BUY)
        print(f"Bought [ {quantity} ] of [ {stock_symbol} ]")
    except APIError as error:
        print(f"Buy Order Error: {error.status_code} - ",json.loads(str(error))["message"])
        sys.exit(1)


def marker_sell_order(stock_symbol,quantity, client):
    try:
        market_order(stock_symbol,quantity,client,OrderSide.SELL)
        print(f"Sold [ {quantity} ] of [ {stock_symbol} ]")
    except APIError as error:
        print(f"Sell Order Error: {error.status_code} - ",json.loads(str(error))["message"] )
        sys.exit(1)


