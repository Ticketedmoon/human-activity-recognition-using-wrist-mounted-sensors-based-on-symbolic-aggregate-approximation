from unittest.mock import MagicMock
import unittest 
import sys

# Path is viewed from where run_tests.py is
sys.path.append('./code/machine_learning_module/')

from logger_module.Logger import Logger
from bitmap_generator import BitmapGenerator

# Note If you mistype assert_called_with (to assert_called_once 
# or {typo_here}) your test may still run, as Mock will 
# think this is a mocked function and happily go along, unless 
#you use autospec=true.
class Test_Bitmap_Generation(unittest.TestCase):

    def test_build(self):
        generator = BitmapGenerator(logger_path="./code/")
        generator.generate_bitmaps = MagicMock()
        generator.build()
        assert generator.generate_bitmaps.call_count == 4

    # @mock.patch('bitmap_generator.')
    # def test_generate_bitmaps(self):
    #     generator = BitmapGenerator(logger_path="./code/")
    #     generator.generate_bitmaps



if __name__ == "__main__":
    unittest.main()