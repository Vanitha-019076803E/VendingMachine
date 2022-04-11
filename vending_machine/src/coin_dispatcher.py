from coin_processor import CoinProcessor
from monitor import Monitor

class CoinDispatcher():
    '''Return Coins'''

    def __init__(self, coin_processor: CoinProcessor, monitor: Monitor):
        self.coin_processor = coin_processor
        self.monitor = monitor

    def dispatch(self, amount=None):
        is_return_amount = False #it is to handle separate message for getting back the whole amount in return using "RETURN COINS" command
        if(amount == None):
            is_return_amount = True
            amount = self.coin_processor.current_amount
        change_list = self.coin_processor.make_change(amount)
        for change in change_list:
            self.coin_processor.reduce_coin(change)
        self.coin_processor.reset_current_balance()
        if(is_return_amount):
            self.coin_processor.reset_current_balance()
            self.monitor.display('Money returned\n')
            self.monitor.display('INSERT COIN')
        else:
            self.monitor.display(
                f'please take your change {amount}€')


    
