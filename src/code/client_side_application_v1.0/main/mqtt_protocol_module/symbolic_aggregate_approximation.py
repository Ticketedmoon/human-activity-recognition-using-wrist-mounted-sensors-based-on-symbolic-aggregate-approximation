import sys
import numpy as np
import pandas as pd

# Train Mode
sys.path.append("../")

# Test Mode
# sys.path.append("../../")
from logger_module.Logger import Logger

from sax_module.time_series_to_string_via_sax import Time_series_to_string_via_sax

class SymbolicAggregateApproximation:

    training_exercise_path = "../../resources/exercise-datasets"
    letter_size = 20
    horizontal_window_property = 1

    def __init__(self, logger=True):
        if (logger):
            self.logger = Logger("../", "logs/Symbolic")
            self.logger.info("Symbolic Aggregate Approximation Object Created...")

        self.sax_obj = Time_series_to_string_via_sax()

    # General Abstract Generate method; unsure of the activity; useful for server.
    def generate(self, filename):
        return self.sax_obj.generate_string_from_time_series(filename, self.letter_size, self.horizontal_window_property)

    def get_data_vector_properties(self, csv_path):
        return self.sax_obj.get_data_vector_properties(csv_path)

    def generate_real_time(self, data_store):
        data = np.array(data_store) 
        series = pd.Series(data)
        return self.sax_obj.build_string_from_numpy_data(series, self.letter_size, self.horizontal_window_property)

    def generate_all_activities_as_string_representation(self, subjectNo):
        return[self.generate_walk(subjectNo), self.generate_run(subjectNo), self.generate_low_bike(subjectNo), self.generate_high_bike(subjectNo)]

    def generate_walk(self, subjectNo):
        try:
            walk_path = "{}/Walk-subject-{}.csv".format(self.training_exercise_path, subjectNo)
            exercise_results = self.sax_obj.generate_string_from_time_series(walk_path, self.letter_size, self.horizontal_window_property)
            return exercise_results
        except:
            return ""

    def generate_run(self, subjectNo):
        try:
            run_path = "{}/Run-subject-{}.csv".format(self.training_exercise_path, subjectNo)
            exercise_results = self.sax_obj.generate_string_from_time_series(run_path, self.letter_size, self.horizontal_window_property)
            return exercise_results
        except:
            return ""

    def generate_low_bike(self, subjectNo):
        try:
            low_bike_path = "{}/LowResistanceBike-subject-{}.csv".format(self.training_exercise_path, subjectNo)
            exercise_results = self.sax_obj.generate_string_from_time_series(low_bike_path, self.letter_size, self.horizontal_window_property)
            return exercise_results
        except:
            return ""

    def generate_high_bike(self, subjectNo):
        try:
            high_bike_path = "{}/HighResistanceBike-subject-{}.csv".format(self.training_exercise_path, subjectNo)
            exercise_results = self.sax_obj.generate_string_from_time_series(high_bike_path, self.letter_size, self.horizontal_window_property)
            return exercise_results
        except:
            return ""

if __name__ == "__main__":
    sax_obj = SymbolicAggregateApproximation(True)