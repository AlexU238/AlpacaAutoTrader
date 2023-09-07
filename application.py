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

print("Loggin in...")
configuration.get_configuration_info("config.txt")

client_manager=client.ClientLoginManager(client.TradingClientLogin())
trade_client=client_manager.logInClient(configuration.module_values["API_KEY"],configuration.module_values["SECRET"],True)
client_manager=client.ClientLoginManager(client.StockHistoricalDataClientLogin())
stock_client=client_manager.logInClient(configuration.module_values["API_KEY"],configuration.module_values["SECRET"])
print("Login successful!\n")

print("Account data:")
account.check_account_data(trade_client)

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
    except Exception as e:
        print("Error: ",e)
        break