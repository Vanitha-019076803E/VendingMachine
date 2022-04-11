# VendingMachine

## Requirements to run the application
1. Python Version 3.9 
2. coverage installed through pip (`pip install coverage`)



## Running the application
1. Execute the following command inside `VendingMachine/vending_machine/src/`
`python main.py`

2. You would see the CLI showing the following


## To run the test cases
1. Install coverage with pip using the command `pip install coverage`
2. Execute the following command inside `VendingMachine/vending_machine/test/`

`coverage run -m unittest`
3. There are 27 unit tests available for the application
4. To see the test coverage report, run the following command
`coverage report -m --omit=test.py,test_coin_processor.py,test_command_center.py,test_util_functions.py,test_customer_use_cases.py,test_command_validation.py`
Also, the above command omits the test files while computing the test coverage percentage.
5. This is the coverage report generated by that command
