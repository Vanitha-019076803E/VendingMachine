from decimal import *
from monitor import Monitor
from util import sub_list_sum

class CoinProcessor():
    '''Accept Coins'''

    def __init__(self, valid_coin_denominations: set, monitor: Monitor, vending_machine_balance: dict, current_amount=Decimal("0.0")):
        self.valid_coin_denominations = valid_coin_denominations
        self.monitor = monitor
        self.vending_machine_balance = vending_machine_balance
        self.current_amount = current_amount
        
    def accept_coin(self, entered_amount):
        if(entered_amount not in self.valid_coin_denominations):
            self.monitor.display("Please insert valid coin")
        else:
            self.current_amount = self.current_amount + \
                Decimal(str(entered_amount))
            self.vending_machine_balance[entered_amount] = self.vending_machine_balance.get(
                entered_amount, 0)+1
            self.monitor.display(f"Amount entered {self.current_amount}€")
        
    def reduce_coin(self, coin):
        self.vending_machine_balance[coin]-=1
        if(self.vending_machine_balance[coin])==0:
            del self.vending_machine_balance[coin]
            
    def make_change(self, balance_amount):
        if balance_amount==0:
            return []
        total_coins_list = [value*[key] for key, value in self.vending_machine_balance.items()]
        total_coins = [coin for coin_sub_list in total_coins_list for coin in coin_sub_list]
        dispatch_coins = sub_list_sum(total_coins, balance_amount)
        return dispatch_coins
    
    def reset_current_balance(self):
        self.current_amount = Decimal("0.0")
        

