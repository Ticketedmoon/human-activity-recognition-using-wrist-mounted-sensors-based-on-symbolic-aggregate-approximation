import numpy as np
import pandas as pd

from saxpy.znorm import znorm
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize

walk_csv_path = "../../resources/exercise-datasets/Walk01.csv"
run_csv_path = "../../resources/exercise-datasets/Run01.csv"

walk_data = pd.read_csv(walk_csv_path, index_col=0, parse_dates=True)
run_data = pd.read_csv(run_csv_path, index_col=0, parse_dates=True)

walk_stats = pd.Series(walk_data.values.squeeze())
run_stats = pd.Series(run_data.values.squeeze())

walk_data = pd.to_numeric(walk_stats, errors='coerce')
run_data = pd.to_numeric(run_stats, errors='coerce')

walk_results = ts_to_string(znorm(walk_data), cuts_for_asize(5))
run_results = ts_to_string(znorm(run_data), cuts_for_asize(5))

print("======= WALK RESULTS =========")
print(walk_results)
print("\n\n\n")
print("======= RUN RESULTS ========")
print(run_results)
