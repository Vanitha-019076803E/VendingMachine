from decimal import Decimal
from xmlrpc.client import Boolean
from coin_processor import CoinProcessor
from monitor import Monitor

class ProductSelector():
    '''Select Product'''

    def __init__(self, products: dict, coin_processor: CoinProcessor, monitor: Monitor):
        self.products = products
        self.coin_processor = coin_processor
        self.shown_sold_out = set()
        self.monitor = monitor
        
    def select_product(self, product_number) -> bool:
        selected_product_price = self.products[product_number].price
        selected_product_quantity = self.products[product_number].quantity
        
        if(self.coin_processor.current_amount == 0.00):
            self.monitor.display("INSERT COIN")
            return False
            
        elif(selected_product_quantity == 0):
            if(product_number not in self.shown_sold_out):
                self.shown_sold_out.add(product_number)
                self.monitor.display("SOLD OUT")
            elif(product_number in self.shown_sold_out):
                if(self.coin_processor.current_amount > 0.00):
                    self.monitor.display(
                        f'Remaining money {self.coin_processor.current_amount}€')
            return False

        elif(selected_product_quantity > 0 and self.coin_processor.current_amount >= selected_product_price ):
            balance_amount = self.coin_processor.current_amount - \
                Decimal(str(selected_product_price))
            if(self.coin_processor.make_change(
                balance_amount)!=None):
                return True
            else:
                self.monitor.display('EXACT CHANGE ONLY')
                return False
            
        elif(selected_product_quantity > 0 and 0.00 < self.coin_processor.current_amount < selected_product_price):
            self.monitor.display(
                f"Current amount {self.coin_processor.current_amount}€")
            self.monitor.display(f"PRICE {selected_product_price}€")
            return False
            
        else:
            self.monitor.display("INSERT COIN")
            return False

            
        
