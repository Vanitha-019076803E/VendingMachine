import sys
from unittest import mock
from unittest.mock import patch
sys.path.insert(0, '../src')
from decimal import Decimal
import unittest
from product import Product
from vending_machine import VendingMachine
from command_center import Command


class TestCustomerUseCases(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(TestCustomerUseCases, self).__init__(methodName)
        self.products = {
            1: Product("COLA", Decimal("1"), 0),
            2: Product("Chips",  Decimal("0.50"), 10),
            3: Product("Candy", Decimal("0.75"), 20),
        }
        self.valid_coin_denominations = set((0.05, 0.1, 0.2, 0.5, 1, 2))
        self.vending_machine_balance = {
            0.05: 1,
            0.2: 1
        }
        
    def test_vending_machine_init(self):
        print("************************** test_vending_machine_init [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        self.assertEqual(vending_machine.products, self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print(
            "************************** test_vending_machine_init [END] **************************\n")
    
    def test_enter_valid_coin_denomination(self):
        print("************************** test_enter_valid_coin_denomination [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 1.0€'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance, {
                         0.05: 1, 0.2: 1, 1.0: 1}, "Incorrect vending machine balance")
        print("************************** test_enter_valid_coin_denomination [END] **************************\n")
        
    def test_enter_invalid_coin_denomination(self):
        print("************************** test_enter_invalid_coin_denomination [START] **************************")
        vending_machine = VendingMachine(
        self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["5"]))
        self.assertEqual(vending_machine.monitor.display_log, ['Please insert valid coin'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance, self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_enter_invalid_coin_denomination [END] **************************\n")
        
    def test_valid_return_coin(self):
        print("************************** test_valid_return_coin [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.RETURN, ["COINS"]))        
        self.assertEqual(vending_machine.monitor.display_log,  [
                         'Amount entered 1.0€', 'Money returned\n', 'INSERT COIN'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance, {
                        0.05: 1, 0.2: 1}, "Incorrect vending machine balance")
        print("************************** test_valid_return_coin [END] **************************\n")
    
    
    def test_valid_product_buy(self):
        print("************************** test_valid_product_buy [START] **************************")
        vending_machine_balance = {
            0.5: 1,
            0.2: 1
        }
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.SELECT, ["2"]))
        new_product_list = {
            1: Product("COLA", Decimal("1"), 0),
            2: Product("Chips",  Decimal("0.50"), 9),
            3: Product("Candy", Decimal("0.75"), 20),
        }
        self.assertEqual(vending_machine.monitor.display_log, ['Amount entered 1.0€', 'The product is dispensed',
                                                               'please take your change 0.50€', 'THANK YOU'], "Incorrect message displayed")
        for key, product in vending_machine.products.items():
            self.assertEqual(product.quantity,
                             new_product_list[key].quantity, "Incorrect products quantity after buying in vending machine")
            
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance, {0.2:1, 1.0:1}, "Incorrect vending machine balance after buying product in vending machine")
        print("************************** test_valid_product_buy [END] **************************\n")
        
    
    def test_invalid_product_buy_for_unavailable_change(self):
        print("************************** test_invalid_product_buy_for_unavailable_change [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.SELECT, ["2"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 1.0€', 'EXACT CHANGE ONLY'], "Incorrect message displayed")
        for key, product in vending_machine.products.items():
            self.assertEqual(product.quantity,
                             self.products[key].quantity, "Incorrect products quantity after not buying because of unavailable change in vending machine")
        print("************************** test_invalid_product_buy_for_unavailable_change [END] **************************\n")
    
    
    def test_invalid_product_buy_for_unavailable_product(self):
        print("************************** test_invalid_product_buy_for_unavailable_product [START] **************************")
        vending_machine = VendingMachine(
        self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.SELECT, ["1"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 1.0€', 'SOLD OUT'], "Incorrect message displayed")
        for key, product in vending_machine.products.items():
            self.assertEqual(product.quantity, self.products[key].quantity, "Incorrect products quantity after not buying because of unavailable product in vending machine")
        print("************************** test_invalid_product_buy_for_unavailable_product [END] **************************\n")
        
        
    def test_invalid_product_buy_for_unavailable_product_and_get_back_money(self):
        print("************************** test_invalid_product_buy_for_unavailable_product_and_get_back_money [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.SELECT, ["1"]))
        vending_machine.execute_command((Command.RETURN, ["coins"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 1.0€', 'SOLD OUT', 'Enter valid Command. For e.g., RETURN COINS'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance, self.vending_machine_balance,
                             "Incorrect vending machine balance after not buying because of unavailable product")
        print("************************** test_invalid_product_buy_for_unavailable_product_and_get_back_money [END] **************************\n")
    
    @patch("builtins.input", return_value="TERMINATE")
    def test_starting_vending_machine(self, mock_input):
        print("************************** test_starting_vending_machine [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        
        vending_machine.start()
        self.assertEqual(vending_machine.monitor.display_log, ['Welcome!!!\nHow may I help you?',
                                                               'Thank you for using our Vending Machine\nTerminated'], "Incorrect message displayed")
        
        self.assertEqual(vending_machine.products,
                         self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_starting_vending_machine [END] **************************\n")
    
    def test_valid_show_command(self):
        print("************************** test_valid_show_command [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.SHOW, []))
        self.assertEqual(vending_machine.monitor.display_log, [
                         '1. COLA  1€ - SOLD OUT', '2. Chips  0.50€ - 10 items left', '3. Candy  0.75€ - 20 items left'], "Incorrect message displayed")
        self.assertEqual(vending_machine.products,
                         self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_valid_show_command [END] **************************\n")
    
    
    def test_insufficient_product_quantity(self):
        print("************************** test_insufficient_product_quantity [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)

        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.SELECT, ["1"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 1.0€', 'SOLD OUT'], "Incorrect message displayed")
        self.assertEqual(vending_machine.products,
                         self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_insufficient_product_quantity [END] **************************\n")
        
    
    def test_zero_current_amount(self):
        print("************************** test_zero_current_amount [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)

        vending_machine.execute_command((Command.SELECT, ["1"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'INSERT COIN'], "Incorrect message displayed")
        self.assertEqual(vending_machine.products,
                         self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_zero_current_amount [END] **************************\n")
    
    def test_insufficient_current_amount(self):
        print("************************** test_insufficient_current_amount [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["0.1"]))
        vending_machine.execute_command((Command.SELECT, ["2"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 0.1€', 'Current amount 0.1€', 'PRICE 0.50€'], "Incorrect message displayed")
        self.assertEqual(vending_machine.products,
                         self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_insufficient_current_amount [END] **************************\n")

if __name__ == '__main__':
    unittest.main()
