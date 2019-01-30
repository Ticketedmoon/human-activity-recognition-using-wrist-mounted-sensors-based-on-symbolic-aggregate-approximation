import pandas as pd

from saxpy.znorm import znorm
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize

class SymbolicAggregateApproximation:

    exercise_path = "../../resources/exercise-datasets/"

    def generate_walk(self, file_no):
        walk_data = pd.read_csv(self.exercise_path + "Walk0" + str(file_no) + ".csv",
                                index_col=0, parse_dates=True, skiprows=[0, 1])
        print(walk_data)
        walk_stats = pd.Series(walk_data.values.squeeze())
        numeric_data = pd.to_numeric(walk_stats, errors='coerce')
        return self.apply_sax_transformation(numeric_data)

    def generate_run(self, file_no):
        run_data = pd.read_csv(self.exercise_path + "Run0" + str(file_no) + ".csv",
                               index_col=0, parse_dates=True, skiprows=[0, 1])
        run_stats = pd.Series(run_data.values.squeeze())
        numeric_data = pd.to_numeric(run_stats, errors='coerce')
        return self.apply_sax_transformation(numeric_data)

    def generate_low_bike(self, file_no):
        low_bike_data = pd.read_csv(self.exercise_path + "LowResistanceBike0" + str(file_no) + ".csv",
                                    index_col=0, parse_dates=True, skiprows=[0, 1])
        low_bike_stats = pd.Series(low_bike_data.values.squeeze())
        numeric_data = pd.to_numeric(low_bike_stats, errors='coerce')
        return self.apply_sax_transformation(numeric_data)

    def generate_high_bike(self, file_no):
        high_bike_data = pd.read_csv(self.exercise_path + "HighResistanceBike0" + str(file_no) + ".csv",
                                     index_col=0, parse_dates=True, skiprows=[0, 1])
        high_bike_stats = pd.Series(high_bike_data.values.squeeze())
        numeric_data = pd.to_numeric(high_bike_stats, errors='coerce')
        return self.apply_sax_transformation(numeric_data)

    @staticmethod
    def apply_sax_transformation(data):
        cut_size = cuts_for_asize(10)
        exercise_results = ts_to_string(znorm(data), cut_size)
        return exercise_results

def main():
    sax_obj = SymbolicAggregateApproximation()
    print_demo(sax_obj, 1)

def print_demo(sax_obj, file_no):
    try:
        print(" -- Walk Results --")
        print(sax_obj.generate_walk(file_no))

        print(" -- Run Results --")
        print(sax_obj.generate_run(file_no))

        print(" -- Low Resistance Bike Results --")
        print(sax_obj.generate_low_bike(file_no))

        print(" -- High Resistance Bike Results --")
        print(sax_obj.generate_high_bike(file_no))

    except FileNotFoundError:
        print("File with ID: 0" + str(file_no) + " Not Found")

if __name__ == "__main__":
    main()
