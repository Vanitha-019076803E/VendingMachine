
from decimal import Decimal

from product import Product
from vending_machine import VendingMachine



if __name__ == "__main__":
    
    products = {
        1: Product( "COLA", Decimal("1"), 0),
        2: Product("Chips",  Decimal("0.50"), 10),
        3: Product("Candy", Decimal("0.75"), 20),
    }
    valid_coin_denominations = set((0.05, 0.1, 0.2, 0.5, 1, 2))
    vending_machine_balance = {
        coin_denomination: 10 for coin_denomination in valid_coin_denominations}
    # vending_machine_balance = {
    #     0.05: 1,
    #     # 0.2:1
    # }
    vending_machine = VendingMachine(
        products, valid_coin_denominations=valid_coin_denominations, vending_machine_balance=vending_machine_balance)

    vending_machine.start()
