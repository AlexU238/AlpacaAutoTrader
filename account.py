#-------------------------------------------------------------------------------------------
# Name:        account
# Purpose:     manages account related information
#
# Author:      U238 (https://github.com/AlexU238)
#
# Last Edit:   10/09/2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#-------------------------------------------------------------------------------------------
import json

account_permissions={
'account_status':"",
'buying_power':0.0,
'day_trade_buy_power':0.0,
'trading_blocked': False,
'account_blocked': False
}


def get_account_data(client):
    try:
        account_info=dict(client.get_account())
    except APIError as error:
        error=json.loads(str(error))["message"]
        print(f"\033[91mAccount Error: {error.status_code} {error}\033[0m")
        sys.exit(1)
    account_permissions["account_status"]=account_info["status"].split('.')[0]
    account_permissions["buying_power"]=float(account_info["buying_power"].strip())
    account_permissions["day_trade_buy_power"]=float(account_info["daytrading_buying_power"].strip())
    account_permissions["trading_blocked"]=account_info["trading_blocked"]
    account_permissions["account_blocked"]=account_info["account_blocked"]

    print("Account data:")
    for k,v in account_info.items():
        print(f"{k:30}{v}")

