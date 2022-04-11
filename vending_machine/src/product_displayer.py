from monitor import Monitor

class ProductDisplayer():
    '''Show Products'''
    
    def __init__(self, products: dict, monitor: Monitor):
        self.products = products
        self.monitor = monitor
        
    def display_products(self):
        for key, product in self.products.items():
            if(product.quantity != 0):
                self.monitor.display(
                    f'{key}. {product.name}  {product.price}€ - {product.quantity} items left')
            else:
                self.monitor.display(
                    f'{key}. {product.name}  {product.price}€ - SOLD OUT')
