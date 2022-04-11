import sys
sys.path.insert(0, '../src')
from command_center import Command, CommandCenter
import unittest
from unittest.mock import patch


class TestCommandCenter(unittest.TestCase):
    
    @patch("builtins.input", return_value="ENTER 2")
    def test_get_command(self, mock_input):
        print(
            "************************** test_get_command [START] **************************")
        command_center = CommandCenter()
        command = command_center.get_command()
        self.assertEqual(command[0], Command.ENTER,
                         "Incorrect command returned")
        self.assertEqual(command[1], ["2"],
                         "Incorrect command arguments")
        print(
            "************************** test_get_command [END] **************************\n")
        
    @patch("builtins.input", return_value="")
    def test_new_line_command(self, mock_input):
        print("************************** test_new_line_command [START] **************************")
        command_center = CommandCenter()
        command = command_center.get_command()
        self.assertEqual(command[0], Command.NEW_LINE,
                         "Incorrect command returned")
        self.assertEqual(command[1], [],
                         "Incorrect command arguments")
        print("************************** test_new_line_command [END] **************************\n")

if __name__ == '__main__':
    unittest.main()
