
import sys
from unittest import mock
sys.path.insert(0, '../src')
from decimal import Decimal
import unittest
from command_center import Command
from product import Product
from vending_machine import VendingMachine


class TestCommandValidation(unittest.TestCase):
    
    def __init__(self, methodName='runTest'):
        super(TestCommandValidation, self).__init__(methodName)
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
        
    def test_invalid_enter_command(self):
        print(
            "************************** test_invalid_enter_command [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["one"]))
        self.assertEqual(vending_machine.monitor.display_log,  [
            'Enter valid Command. For e.g., ENTER 1'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                        self.vending_machine_balance, "Incorrect vending machine balance")
        print(
            "************************** test_invalid_enter_command [END] **************************\n")

    
    def test_invalid_return_command(self):
        print(
            "************************** test_invalid_return_command [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.RETURN, []))
        self.assertEqual(vending_machine.monitor.display_log,  [
                         'Amount entered 1.0€', 'Enter valid Command. For e.g., RETURN COINS'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance, {
            0.05: 1, 0.2: 1, 1.0: 1}, "Incorrect vending machine balance")
        print(
            "************************** test_invalid_return_command [END] **************************\n")
    
    
    def test_invalid_return_coin_without_enter_coin(self):
        print("************************** test_invalid_return_coin_without_enter_coin [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, []))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'INSERT COIN'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_invalid_return_coin_without_enter_coin [END] **************************\n")
    
    
    def test_empty_product_number_in_select_command(self):
        print("************************** test_empty_product_number_in_select_command [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.SELECT, []))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 1.0€', 'Enter Product number after SELECT command'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_empty_product_number_in_select_command [END] **************************\n")
    
    
    def test_invalid_product_number_select_command(self):
        print("************************** test_invalid_product_number_select_command [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.ENTER, ["1"]))
        vending_machine.execute_command((Command.SELECT, ["productnumber"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Amount entered 1.0€', 'Enter valid Command. For e.g., SELECT 1'], "Incorrect message displayed")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_invalid_product_number_select_command [END] **************************\n")
    
    
    def test_invalid_show_command(self):
        print("************************** test_invalid_show_command [START] **************************")
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        vending_machine.execute_command((Command.SHOW, ["products"]))
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Enter valid Command. For e.g., SHOW'], "Incorrect message displayed")
        self.assertEqual(vending_machine.products,
                         self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_invalid_show_command [END] **************************\n")
    
    
    def test_invalid_command(self):
        print("************************** test_invalid_command [START] **************************")
        mock_args = ["ABC", "TERMINATE"]
        vending_machine = VendingMachine(
            self.products, valid_coin_denominations=self.valid_coin_denominations, vending_machine_balance=self.vending_machine_balance)
        with mock.patch('builtins.input', side_effect=mock_args):
            vending_machine.start()
        self.assertEqual(vending_machine.monitor.display_log, [
                         'Welcome!!!\nHow may I help you?', 'Invalid Command\n\nAvailable commands are\n\t1. ENTER\n\t2. SHOW\n\t3. SELECT\n\t4. RETURN\n', 'Thank you for using our Vending Machine\nTerminated'], "Incorrect message displayed")
        self.assertEqual(vending_machine.products,
                         self.products, "Incorrect products value")
        self.assertEqual(vending_machine.coin_processor.valid_coin_denominations,
                         self.valid_coin_denominations, "Incorrect valid coin denominations")
        self.assertEqual(vending_machine.coin_processor.vending_machine_balance,
                         self.vending_machine_balance, "Incorrect vending machine balance")
        print("************************** test_invalid_command [END] **************************\n")

if __name__ == '__main__':
    unittest.main()
