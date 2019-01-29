import pandas as pd

from saxpy.znorm import znorm
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize


class Sax:

    walk_csv_path = "../../../resources/exercise-datasets/Walk01.csv"
    run_csv_path = "../../../resources/exercise-datasets/Run01.csv"

    def __init__(self):
        self.walk_data = pd.read_csv(self.walk_csv_path, index_col=0, parse_dates=True, skiprows=[0, 1])
        self.run_data = pd.read_csv(self.run_csv_path, index_col=0, parse_dates=True, skiprows=[0, 1])

    def convert_to_single_dim(self):
        walk_stats = pd.Series(self.walk_data.values.squeeze())
        run_stats = pd.Series(self.run_data.values.squeeze())

        walk_data = pd.to_numeric(walk_stats, errors='coerce')
        run_data = pd.to_numeric(run_stats, errors='coerce')
        return walk_data, run_data

    def apply_sax_transformation(self):
        cut_size = cuts_for_asize(12)
        print("letters:   " + str(["a", "b", "c", "d", "e"]))
        print("cut points: " + str(cut_size))

        walk_data, run_data = self.convert_to_single_dim()
        walk_results = ts_to_string(znorm(walk_data), cut_size)
        run_results = ts_to_string(znorm(run_data), cut_size)
        return walk_results, run_results


def main():
    sax_obj = Sax()
    walk_res, run_res = sax_obj.apply_sax_transformation()
    print_demo(walk_res, run_res)


def print_demo(walk_results, run_results):
    print("======= WALK RESULTS =========")
    print(walk_results)
    print()
    print("======= RUN RESULTS ========")
    print(run_results)


if __name__ == "__main__":
    main()
