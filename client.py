#-------------------------------------------------------------------------------------------
# Name:        client
# Purpose:     manages client login
#
# Author:      U238 (https://github.com/AlexU238)
#
# Last Edit:   07/09/2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#-------------------------------------------------------------------------------------------

from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient
import sys

class LoginStrategy:
    def logInClient(self, *args, **kwargs):
        pass

class TradingClientLogin(LoginStrategy):
    def logInClient(self, api_key, secret, is_paper):
        return TradingClient(api_key,secret,paper=is_paper)

class StockHistoricalDataClientLogin(LoginStrategy):
    def logInClient(self, api_key, secret):
        return StockHistoricalDataClient(api_key, secret)

class ClientLoginManager:
    def __init__(self, strategy):
        self.strategy = strategy

    def logInClient(self, *args, **kwargs):
        try:
            return self.strategy.logInClient(*args, **kwargs)
        except ValueError as error:
            print(f"\033[91mClient Error: {error}\033[0m")
            sys.exit(1)
        except Exception as e:
            print(f"\033[91mA Client error has occurred: {str(e)}\033[0m")
            sys.exit(1)
