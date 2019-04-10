import sys

# Train Mode
sys.path.append("../")

# Test Mode
# sys.path.append("../../")
from logger_module.Logger import Logger

from sax_module.time_series_to_string_via_sax import Time_series_to_string_via_sax

class SymbolicAggregateApproximation:

    training_exercise_path = "../../resources/exercise-datasets"
    letter_size = 20

    def __init__(self, logger=True):
        if (logger):
            self.logger = Logger("../", "logs/Symbolic")
            self.logger.info("Symbolic Aggregate Approximation Object Created...")
        self.sax_obj = Time_series_to_string_via_sax()

    # General Abstract Generate method; unsure of the activity; useful for server.
    def generate(self, filename):
        return self.sax_obj.generate_string_from_time_series(filename, self.letter_size, 1)

    def generate_all_activities_as_string_representation(self, subjectNo):
        return[self.generate_walk(subjectNo), self.generate_run(subjectNo), self.generate_low_bike(subjectNo), self.generate_high_bike(subjectNo)]

    def generate_walk(self, subjectNo):
        walk_path = "{}/Walk0{}.csv".format(self.training_exercise_path, subjectNo)
        exercise_results = self.sax_obj.generate_string_from_time_series(walk_path, self.letter_size, 1)
        return exercise_results

    def generate_run(self, subjectNo):
        run_path = "{}/Run0{}.csv".format(self.training_exercise_path, subjectNo)
        exercise_results = self.sax_obj.generate_string_from_time_series(run_path, self.letter_size, 1)
        return exercise_results

    def generate_low_bike(self, subjectNo):
        low_bike_path = "{}/LowResistanceBike0{}.csv".format(self.training_exercise_path, subjectNo)
        exercise_results = self.sax_obj.generate_string_from_time_series(low_bike_path, self.letter_size, 1)
        return exercise_results

    def generate_high_bike(self, subjectNo):
        high_bike_path = "{}/HighResistanceBike0{}.csv".format(self.training_exercise_path, subjectNo)
        exercise_results = self.sax_obj.generate_string_from_time_series(high_bike_path, self.letter_size, 1)
        return exercise_results

def main():
    sax_obj = SymbolicAggregateApproximation(True)