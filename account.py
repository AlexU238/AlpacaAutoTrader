#-------------------------------------------------------------------------------------------
# Name:        account
# Purpose:     manages account related information
#
# Author:      U238 (https://github.com/AlexU238)
#
# Last Edit:   07/09/2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#-------------------------------------------------------------------------------------------
import json

def check_account_data(client):
    try:
        account=dict(client.get_account())
    except APIError as error:
        error=json.loads(str(error))["message"]
        print(f"\033[91mAccount Error: {error.status_code} {error}\033[0m")
        sys.exit(1)

    print("Account data:")
    for k,v in account.items():
        print(f"{k:30}{v}")