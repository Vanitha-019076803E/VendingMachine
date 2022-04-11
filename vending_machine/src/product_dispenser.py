

from coin_dispatcher import CoinDispatcher
from coin_processor import CoinProcessor
from monitor import Monitor


class ProductDispenser:

    def __init__(self, products: dict, monitor: Monitor, coin_processor: CoinProcessor, coin_dispatcher: CoinDispatcher):
        self.products = products
        self.monitor = monitor
        self.coin_processor = coin_processor
        self.coin_dispatcher = coin_dispatcher

    def dispense_product(self, product_number):
        self.monitor.display("The product is dispensed")
        selected_product_quantity = self.products[product_number].quantity
        selected_product_price = self.products[product_number].price
        balance_amount = self.coin_processor.current_amount - selected_product_price
        if(balance_amount!=0):
            self.coin_dispatcher.dispatch(balance_amount)
        new_quantity = selected_product_quantity - 1
        self.products[product_number].quantity = new_quantity
        self.monitor.display('THANK YOU')
