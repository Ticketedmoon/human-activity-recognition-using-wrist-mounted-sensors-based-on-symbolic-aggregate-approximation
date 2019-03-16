import unittest
import sys

sys.path.append('../code/machine_learning_model')

from sax_module.time_series_to_string_via_sax import Time_series_to_string_via_sax

class Test_Symbolic_Aggregate_Approximation(unittest.TestCase):

    # Test idx2Letter method as part of Time_series_to_string_via_sax class
    def test_idx2letter(self):
        
        time_series_obj = Time_series_to_string_via_sax()

        self.assertEqual(time_series_obj.idx2letter(0), 'a')
        self.assertEqual(time_series_obj.idx2letter(1), 'b')
        self.assertEqual(time_series_obj.idx2letter(2), 'c')
        self.assertEqual(time_series_obj.idx2letter(3), 'd')

if __name__ == "__main__":
    unittest.main()