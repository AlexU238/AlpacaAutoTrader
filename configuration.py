#-------------------------------------------------------------------------------------------
# Name:        configuration
# Purpose:     manages configuration info
#
# Author:      U238 (https://github.com/AlexU238)
#
# Last Edit:   07/09/2023
# Copyright:   (c) Oleksii Bilous 2023-present
# License:     MIT License (See https://opensource.org/licenses/MIT)
#-------------------------------------------------------------------------------------------
import ast  # Import ast module for safely parsing the list


module_values = {
    'API_KEY': "",
    'SECRET': "",
    'SYMBOL_LIST': [],
    'BALANCE': 0.0,
    'PROFIT': 0.0
}

def get_configuration_info(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            key, value = line.strip().split('=')
            key = key.strip()
            if key in module_values:
                if key == 'SYMBOL_LIST':
                    module_values[key] = ast.literal_eval(value.strip())
                elif key == 'BALANCE':
                    module_values[key] = float(value.strip())
                elif key == 'PROFIT':
                    module_values[key] = float(value.strip())
                else:
                    module_values[key] = value.strip()


    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(file_path))
    except Exception as e:
        raise Exception("Error reading values from file: {}".format(e))