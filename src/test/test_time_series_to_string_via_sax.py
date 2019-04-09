import unittest
import sys
import pandas as pd

# Path is viewed from where run_tests.py is
sys.path.append('./code/machine_learning_module')

from sax_module.time_series_to_string_via_sax import Time_series_to_string_via_sax

from logger_module.Logger import Logger

class Test_Time_Series_To_String_Via_Sax(unittest.TestCase):

    # Test idx2Letter method as part of Time_series_to_string_via_sax class
    def test_idx2letter(self):
        
        time_series_obj = Time_series_to_string_via_sax()

        self.assertEqual(time_series_obj.idx2letter(0), 'a')
        self.assertEqual(time_series_obj.idx2letter(1), 'b')
        self.assertEqual(time_series_obj.idx2letter(2), 'c')
        self.assertEqual(time_series_obj.idx2letter(3), 'd')

    def test_generate(self):
        time_series_obj = Time_series_to_string_via_sax()
        test_path = "./resources/exercise-datasets/Walk01.csv"
        df = time_series_obj.generate(test_path)
        self.assertTrue(isinstance(df, pd.Series))

    def test_apply_letter_window(self):
        time_series_obj = Time_series_to_string_via_sax()
        test_path = "./resources/exercise-datasets/Walk01.csv"
        data = time_series_obj.generate(test_path)
        windowed_data = time_series_obj.apply_letter_window(data, 1)
        self.assertTrue(isinstance(windowed_data, pd.Series))
        self.assertTrue(windowed_data[0] > 1000)
        self.assertTrue(windowed_data[1] > 1000)

    def test_normalise_data(self):
        time_series_obj = Time_series_to_string_via_sax()
        test_path = "./resources/exercise-datasets/Walk01.csv"
        data = time_series_obj.generate(test_path)
        windowed_data = time_series_obj.apply_letter_window(data, 1)
        normalised_data = time_series_obj.normalise_data(windowed_data)
        self.assertTrue(isinstance(normalised_data, pd.Series))
        self.assertTrue(normalised_data[0] > 0 and normalised_data[0] < 1)
        self.assertTrue(normalised_data[1] > 1)
        self.assertTrue(normalised_data[3] > 0 and normalised_data[3] < 1)

    def test_ts_to_string(self):
        time_series_obj = Time_series_to_string_via_sax()
        test_path = "./resources/exercise-datasets/Walk01.csv"
        sax_string = time_series_obj.generate_string_from_time_series(test_path, 20, 1)
        self.assertTrue(len(sax_string) > 15000)
        condition = ('a' in sax_string and 'b' in sax_string and 'c' in sax_string
                    and 'd' in sax_string and 'e' in sax_string and 'f' in sax_string
                    and 'g' in sax_string and 'h' in sax_string and 'i' in sax_string
                    and 'j' in sax_string and 'k' in sax_string and 'm' in sax_string
                    and 'n' in sax_string and 'o' in sax_string and 'p' in sax_string
                    and 'q' in sax_string and 'r' in sax_string and 's' in sax_string)

        self.assertTrue(condition)
if __name__ == "__main__":
    unittest.main()