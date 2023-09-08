#-------------------------------------------------------------------------------
# Name:        application
# Purpose:     contains the main logic of the program
#
# Author:      U238 ( https://github.com/AlexU238 )
#
# Last Edit:   23d August 2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#-------------------------------------------------------------------------------

import configuration
import client
import account
import utils
import sys
import time
import pytz
from datetime import datetime
import price_info

print("Loggin in...")
configuration.get_configuration_info("config.txt")

client_manager=client.ClientLoginManager(client.TradingClientLogin())
trade_client=client_manager.logInClient(configuration.module_values["API_KEY"],configuration.module_values["SECRET"],True)
client_manager=client.ClientLoginManager(client.StockHistoricalDataClientLogin())
stock_client=client_manager.logInClient(configuration.module_values["API_KEY"],configuration.module_values["SECRET"])
print("Login successful!\n")

print("Account data:")
account.check_account_data(trade_client)
is_just_started=True
is_hold=False
print("\nStarting...")



try:
    position_size = utils.get_usable_balance_per_stock(configuration.module_values["BALANCE"],configuration.module_values["SYMBOL_LIST"])
    work_list=utils.create_stock_use_data_list(configuration.module_values["SYMBOL_LIST"])
except Exception as e:
    print("Error in calculations of balance, price per stock or in creation of symbol list: ", e)
    sys.exit(1)


while True:
    try:
        time_zone=pytz.timezone('Europe/Prague')
        current_time=datetime.now(time_zone)
        formated_current_time = current_time.strftime("%H:%M:%S")

        trading_time=("16:30:00" <= formated_current_time < "23:00:00")

        if trading_time:
            #first_buy
            if is_just_started:
                for stock in work_list:
                    current_price=price_info.get_current_trade_price(stock_client,stock.symbol)
                    if(current_price>position_size):
                        print(f"Insufficient funds to buy {stock.symbol} with {current_price} per stock")
                        stock.amount=-1
                        stock.bought=-1
                        continue
                    stock.amount=utils.get_amount_of_stocks_to_buy(current_price,position_size)
                    print(f"Will attemt to buy {stock.amount} of {stock.symbol}.")
                    orders.marker_buy_order(stock.symbol,stock.amount,client)
                    stock.price=current_price*stock.amount
                    stock.bought=stock.amount
                is_just_started=False
                is_hold=True
                print("First buy concluded.")
            if is_hold:
                print("Hold...")
                for stock in work_list:
                    possible_sell_price=stock.bought*price_info.get_current_trade_price(stock_client,stock.symbol)
                    if(possible_sell_price>=stock.price+1):
                        print("Sell")
                        if stock.bought>0:
                            print(f"Will attemt to sell {stock.amount} of {stock.symbol}.")
                            new_current_price=price_info.get_current_trade_price(stock_client,stock.symbol)
                            orders.marker_sell_order(stock.symbol,stock.bought,client)
                            print("Sold for: ",new_current_price*stock.bought)
                            stock.bought=0
                            stock.price=0
                    else continue



    except Exception as e:
        print("Error: ",e)
        break