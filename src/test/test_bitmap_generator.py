from unittest.mock import MagicMock
import unittest 
import sys
from mock import patch

# Path is viewed from where run_tests.py is
sys.path.append('./code/machine_learning_module/')

from logger_module.Logger import Logger
from bitmap_generator import BitmapGenerator
from symbolic_aggregate_approximation import SymbolicAggregateApproximation
from bitmap_module.rgb_letter_to_colour_conversion import rgb_letter_to_colour
from bitmap_module.greyscale_letter_to_colour_conversion import greyscale_letter_to_colour
from bitmap_module.text_to_bmp_class import Bitmap

# Note If you mistype assert_called_with (to assert_called_once 
# or {typo_here}) your test may still run, as Mock will 
# think this is a mocked function and happily go along, unless 
#you use autospec=true.
class Test_Bitmap_Generation(unittest.TestCase):

    def test_build(self):
        generator = BitmapGenerator(logger_path="./code/", testMode=True)
        generator.generate_bitmaps = MagicMock()
        size = len(generator.train_subjects) + len(generator.test_subjects)
        generator.build()
        assert generator.generate_bitmaps.call_count == size

    def test_generate_bitmaps(self):
        generator = BitmapGenerator(logger_path="./code/", testMode=True)
        generator.generate_bitmaps_for_subject = MagicMock()
        generator.generate_bitmaps("test", 1)
        assert generator.generate_bitmaps_for_subject.call_count == 1

    @patch.object(SymbolicAggregateApproximation, 'generate_all_activities_as_string_representation')
    def test_generate_bitmaps_for_subject(self, test_generate_all_activities_as_string_representation):
        generator = BitmapGenerator(logger_path="./code/", testMode=True)
        subject_no = 1

        generator.generate_all = MagicMock()
        generator.sax_obj = MagicMock()

        generator.generate_bitmaps_for_subject("test", subject_no)
        assert generator.sax_obj.generate_all_activities_as_string_representation.call_count == 1
        assert generator.generate_all.call_count == 4

    def test_generate_all(self):
        generator = BitmapGenerator(logger_path="./code/", testMode=True)
        generator.generate = MagicMock()
        shift = 32
        test_string = "abc" * shift # 96 length string
        generator.generate_all("Walk", test_string, 0, "test")
        self.assertTrue(generator.generate.call_count == 3)

    def test_generate(self):
        generator = BitmapGenerator(logger_path="./code/", testMode=True)
        generator.build_image = MagicMock()
        
        test_activity = "Walk"
        test_string = "aabbcc" * 8 # 48 length string

        generator.generate(test_activity, test_string, 1, 1, 'test')
        self.assertTrue(generator.build_image.call_count == 1)
        self.assertTrue(generator.image_map["test"]["Walk"] == 1)

    def test_build_image(self):
        generator = BitmapGenerator(logger_path="./code/", testMode=True)
        generator.Image = MagicMock()
        generator.bitmap_size = 5

        test_result = generator.build_image(1, 0, "aabbc" * 5) 
        self.assertTrue(isinstance(test_result, Bitmap))

    def test_reset_activity_counter(self):
        generator = BitmapGenerator(logger_path="./code/", testMode=True)
        generator.server_image_counter = 50
        self.assertTrue(generator.server_image_counter == 50)
        generator.reset_activity_counter()
        self.assertTrue(generator.server_image_counter == 0)

if __name__ == "__main__":
    unittest.main()