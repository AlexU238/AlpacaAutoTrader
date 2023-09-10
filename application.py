#-------------------------------------------------------------------------------
# Name:        application
# Purpose:     contains the main logic of the program
#
# Author:      U238 ( https://github.com/AlexU238 )
#
# Last Edit:   10/09/2023
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
import orders

print("Loggin in...")
configuration.get_configuration_info("config.txt")

client_manager=client.ClientLoginManager(client.TradingClientLogin())
trade_client=client_manager.logInClient(configuration.module_values["API_KEY"],configuration.module_values["SECRET"],True)
client_manager=client.ClientLoginManager(client.StockHistoricalDataClientLogin())
stock_client=client_manager.logInClient(configuration.module_values["API_KEY"],configuration.module_values["SECRET"])
print("Login successful!\n")

account.get_account_data(trade_client)
is_just_started=True
print("\nStarting...")



try:
    position_size = utils.get_usable_balance_per_stock(configuration.module_values["BALANCE"],configuration.module_values["SYMBOL_LIST"])
    work_list=utils.create_stock_use_data_list(configuration.module_values["SYMBOL_LIST"])
except Exception as e:
    print("Error in calculations of balance, price per stock or in creation of symbol list: ", e)
    sys.exit(1)

time_zone=pytz.timezone('Europe/Prague')

print(trade_client.get_account().daytrade_count)

while True:
    try:

        if(account.account_permissions["account_status"]!="ACTIVE"): break
        if(account.account_permissions["buying_power"]<1): break
        if(account.account_permissions["day_trade_buy_power"]<1): break
        if(account.account_permissions["trading_blocked"]): break
        if(account.account_permissions["account_blocked"]): break

        trading_time=trade_client.get_clock().is_open
        #("16:30:00" <= formated_current_time < "23:00:00")

        if trading_time:
            #first_buy
            if is_just_started:
                for stock in work_list:
                    current_price=price_info.get_current_trade_price(stock_client,stock.symbol)+0.01
                    if(current_price>position_size):
                        print(f"Insufficient funds to buy {stock.symbol} with {current_price} per stock")
                        stock.amount=-1
                        stock.bought=-1
                        continue
                    stock.amount=utils.get_amount_of_stocks_to_buy(current_price,position_size)
                    print(f"Will attemt to buy {stock.amount} of {stock.symbol} for {current_price}.")
                    orders.marker_buy_order(stock.symbol,stock.amount,trade_client)
                    stock.price=current_price*stock.amount
                    stock.bought=stock.amount
                    stock.is_hold=True
                is_just_started=False
                print("First buy concluded.")
            for stock in work_list:
                if(stock.is_hold):
                    possible_sell_price=stock.bought*price_info.get_current_trade_price(stock_client,stock.symbol)
                    if(possible_sell_price>= stock.price+configuration.module_values["PROFIT"]):
                        print("Sell")
                        if stock.bought>0:
                            print(f"Will attemt to sell {stock.amount} of {stock.symbol}.")
                            new_current_price=price_info.get_current_trade_price(stock_client,stock.symbol)
                            orders.marker_sell_order(stock.symbol,stock.bought,trade_client)
                            print("Sold for: ",new_current_price*stock.bought)
                            stock.bought=0
                            stock.price=0
                            stock.is_hold=False
                    else:
                        print(f"Not profitable to sell {stock.symbol} yet, holding...")
                else:
                    new_current_price=price_info.get_current_trade_price(stock_client,stock.symbol)+0.01
                    if(new_current_price>position_size):
                        print(f"Insufficient funds to buy {stock.symbol} with {new_current_price} per stock")
                        stock.amount=-1
                        stock.bought=-1
                        continue
                    new_bought=utils.get_amount_of_stocks_to_buy(new_current_price,position_size)
                    if(new_bought>=stock.amount):
                        print(f"Will attemt to buy {new_bought} of {stock.symbol}...")
                        orders.marker_buy_order(stock.symbol,new_bought,trade_client)
                        print(f"Bought {new_bought} of {stock.symbol}")
                        stock.bought=new_bought
                        stock.price=new_current_price*new_bought
                        stock.is_hold=True
                    else:
                        print(f"Disadvantageous to buy {stock.symbol}, waiting...")

        else:
            print("Market closed...")

        current_time=datetime.now(time_zone)
        formated_current_time = current_time.strftime("%H:%M:%S")
        print("Time: ", formated_current_time)
        time.sleep(60)
    except Exception as e:
        print("Error: ",e)
        break