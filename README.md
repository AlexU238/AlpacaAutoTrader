# AlpacaAutoTrader
Currently in testing.
Done as a pet project.

Generally for those who don't have time to do market research.

User defines the amount of money they are willing to spend and a list of stocks they want to trade.
The program divides the money given evenly between the items in the list.
Once started, the program will buy the maximum amount of stocks for the money allocated to each of them.
The program then checks the current price of the symbol and multiplyies with the amount of stocks that the user currently has on their account.
If the resulting possible sell price is higher then the price at which the stocks were bought by a user specified amount, the program will sell them.
After sell, the program will attempt to buy the same or higher amount of stocks for the same amount of money which was allocated at the start, thus theoretically keeping the profit.
The process then repeats.
