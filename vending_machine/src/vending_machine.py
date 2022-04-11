
from sre_constants import SUCCESS
from coin_dispatcher import CoinDispatcher
from coin_processor import CoinProcessor
from command_center import Command, CommandCenter
from monitor import Monitor
from product_dispenser import ProductDispenser
from product_displayer import ProductDisplayer
from product_selector import ProductSelector
from util import is_float


class TerminatedError(Exception):
    pass


class VendingMachine:
    '''Main - Vending Machine'''

    def __init__(self, products: dict, valid_coin_denominations: set, vending_machine_balance: dict):
        self.products = products
        self.monitor = Monitor()
        self.command_center = CommandCenter()
        self.coin_processor = CoinProcessor(
            valid_coin_denominations, self.monitor, vending_machine_balance, 0)
        self.product_displayer = ProductDisplayer(products, self.monitor)
        self.product_selector = ProductSelector(
            products, self.coin_processor, self.monitor)
        self.coin_dispatcher = CoinDispatcher(
            self.coin_processor, self.monitor)
        self.product_dispenser = ProductDispenser(
            products, self.monitor, self.coin_processor, self.coin_dispatcher)
    
    def start(self):
        self.monitor.display("Welcome!!!\nHow may I help you?")
        while(1):
            try:
                command = self.command_center.get_command()
                self.execute_command(command)
            except TerminatedError:
                self.monitor.display("Thank you for using our Vending Machine\nTerminated")
                break
            except KeyError:
                self.monitor.display("Invalid Command\n\nAvailable commands are\n\t1. ENTER\n\t2. SHOW\n\t3. SELECT\n\t4. RETURN\n") 
            
   ### Switch case ####
    def execute_command(self, command_obj: tuple):
        command_args = command_obj[1]
        command = command_obj[0]
        
        if(command == Command.TERMINATE):
            raise TerminatedError
            
        elif(command == Command.NEW_LINE):
            self.monitor.display("\n")
            
        elif(command == Command.ENTER):
            if(len(command_args)==0):
                self.monitor.display("INSERT COIN") 
            elif(len(command_args) == 1 and is_float(command_args[0])):
                self.coin_processor.accept_coin(float(command_args[0]))
            else:
                self.monitor.display("Enter valid Command. For e.g., ENTER 1")
                
        elif(command == Command.SHOW):
            if(len(command_args) > 0):
                self.monitor.display("Enter valid Command. For e.g., SHOW")
            else:
                self.product_displayer.display_products()
        
        elif(command == Command.SELECT):
            if(len(command_args) == 0):
                self.monitor.display("Enter Product number after SELECT command")
            elif(len(command_args) == 1 and is_float(command_args[0])):
                product_number = int(command_args[0])
                is_valid_selection = self.product_selector.select_product(
                    product_number)
                if(is_valid_selection):
                    self.product_dispenser.dispense_product(product_number)
            else:
                self.monitor.display("Enter valid Command. For e.g., SELECT 1")
                
        elif(command == Command.RETURN):
            if(self.coin_processor.current_amount > 0):
                if(len(command_args) == 0 or (len(command_args) == 1 and command_args[0] != "COINS") or len(command_args) > 1):
                    self.monitor.display("Enter valid Command. For e.g., RETURN COINS")
                else:
                    self.coin_dispatcher.dispatch()
            else:
                self.monitor.display("INSERT COIN") 
                           
        else:
            self.monitor.display("Invalid Command")
