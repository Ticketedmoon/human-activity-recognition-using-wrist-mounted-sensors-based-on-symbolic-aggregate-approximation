import unittest
import sys

sys.path.append('../code/machine_learning_model')

from symbolic_aggregate_approximation import SymbolicAggregateApproximation
from sax_module.time_series_to_string_via_sax import Time_series_to_string_via_sax
from logger_module.Logger import Logger

class Test_Symbolic_Aggregate_Approximation(unittest.TestCase):

    # If correctly initialized, object should be Time_series_to_string_via_sax object
    def test_init(self):
        obj = SymbolicAggregateApproximation(False)
        sax_obj = obj.sax_obj

        self.assertIsNotNone(sax_obj)
        self.assertIsInstance(sax_obj, Time_series_to_string_via_sax)

    # Generate Walk test, string > 15300 characters
    def test_generate_walk(self):
        sax_obj = SymbolicAggregateApproximation(False)
        sax_obj.training_exercise_path = "./resources/exercise-datasets/"
        test_results = sax_obj.generate_walk(1)
        self.assertTrue(len(test_results) > 15300)

    # Generate Run test, string > 15300 characters
    def test_generate_run(self):
        sax_obj = SymbolicAggregateApproximation(False)
        sax_obj.training_exercise_path = "./resources/exercise-datasets/"
        test_results = sax_obj.generate_run(1)
        self.assertTrue(len(test_results) > 15300)

    # Generate Low Resistance Bike test, string > 15300 characters
    def test_generate_low_bike(self):
        sax_obj = SymbolicAggregateApproximation(False)
        sax_obj.training_exercise_path = "./resources/exercise-datasets/"
        test_results = sax_obj.generate_low_bike(1)
        self.assertTrue(len(test_results) > 15300)

    # Generate High Resistance Bike test, string > 15300 characters
    def test_generate_high_bike(self):
        sax_obj = SymbolicAggregateApproximation(False)
        sax_obj.training_exercise_path = "./resources/exercise-datasets/"
        test_results = sax_obj.generate_high_bike(1)
        self.assertTrue(len(test_results) > 15300)

if __name__ == "__main__":
    unittest.main()