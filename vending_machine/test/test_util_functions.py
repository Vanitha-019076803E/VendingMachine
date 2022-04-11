import sys
sys.path.insert(0, '../src')
import unittest
from util import is_float, sub_list_sum


class TestUtilFunctions(unittest.TestCase):
    
    def test_sub_list_sum(self):
        print("************************** test_sub_list_sum [START] **************************")
        list = [1, 2, 3, 4, 5]
        sub_list = sub_list_sum(list, 6)
        self.assertEqual(sub_list, [1,2,3],
                         "Incorrect sub list sum")
        print(
            "************************** test_sub_list_sum [END] **************************\n")
        
    
    def test_float(self):
        print("************************** test_float [START] **************************")
        is_float_value= is_float("Hello")
        self.assertEqual(is_float_value, False,
                         "Incorrect float value")
        print(
            "************************** test_float [END] **************************\n")
    
    
    def test_non_float(self):
        print("************************** test_non_float [START] **************************")
        is_float_value= is_float("32")
        self.assertEqual(is_float_value, True,
                         "Incorrect float value")
        print(
            "************************** test_non_float [END] **************************\n")
    
if __name__ == '__main__':
    unittest.main()
