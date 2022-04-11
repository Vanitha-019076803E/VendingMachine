import sys
sys.path.insert(0, '../src')
from command_center import Command
from vending_machine import VendingMachine
import unittest
from decimal import Decimal
from product import Product


class TestCoinProcessor(unittest.TestCase):
    
    def __init__(self, methodName='runTest'):
        super(TestCoinProcessor, self).__init__(methodName)
        self.products = {
            1: Product("COLA", Decimal("1"), 0),
            2: Product("Chips",  Decimal("0.50"), 10),
            3: Product("Candy", Decimal("0.75"), 20),
        }
        self.valid_coin_denominations = set((0.05, 0.1, 0.2, 0.5, 1, 2))

    def test_make_change_for_exact_customer_input_coins(self):
        print("************************** test_make_change_for_exact_customer_input_coins [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance={})
        vending_machine.execute_command((Command.ENTER, ["0.5"]))
        vending_machine.execute_command((Command.SELECT, ["2"]))
        self.assertEqual(vending_machine.coin_processor.make_change(Decimal("0.0")), 
                         [], "Incorrect vending machine balance")
        print("************************** test_make_change_for_exact_customer_input_coins [END] **************************\n")
    
    
    def test_make_change_for_valid_coins_and_get_back_valid_change(self):
        print("************************** test_make_change_for_valid_coins_and_get_back_valid_change [START] **************************")
        vending_machine_balance = {
            0.1:6,
            0.2:2,
        }
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        change_list = vending_machine.coin_processor.make_change(Decimal("1"))
        self.assertEqual(sum(change_list),Decimal("1.0"), "Incorrect vending machine balance")
        print("************************** test_make_change_for_valid_coins_and_get_back_valid_change [END] **************************\n")
        
if __name__ == '__main__':
    unittest.main()
