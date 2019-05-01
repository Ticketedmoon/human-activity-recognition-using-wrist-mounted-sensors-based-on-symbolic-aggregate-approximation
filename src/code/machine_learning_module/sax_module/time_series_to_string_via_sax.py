import pandas as pd
import numpy as np 

from sax_module.norm_sax_letter_conversion import norm_letter_conversion
from sax_module.interval_sax_letter_conversion import int_letter_conversion

class Time_series_to_string_via_sax:

    def generate(self, file_path):
        data = pd.read_csv(file_path, index_col=0, parse_dates=True, skiprows=[0])
        stats = pd.Series(data.values.squeeze())
        numeric_data = pd.to_numeric(stats, errors='coerce')
        return numeric_data

    def apply_letter_window(self, ts_data, window_size):
        average_window_values = []
        for i in range(0, len(ts_data), window_size):
            windowed_data = ts_data[i:i+window_size]
            avg_win_val = sum(windowed_data.values) / window_size
            average_window_values.append(avg_win_val)
        return pd.Series(average_window_values)

    def normalise_data(self, data, threshold=0.01):
        sd = np.std(data)
        if (sd < threshold):
            return data
        mean = np.mean(data)
        return (data - mean) / sd

    def ts_to_string(self, series, cuts):
        a_size = len(cuts)
        sax = list()
        for i in range(0, len(series)):
            num = series[i]
            if(num >= 0):
                j = a_size - 1
                while ((j > 0) and (cuts[j] >= num)):
                    j = j - 1
                sax.append(self.idx2letter(j))
            else:
                j = 1
                while (j < a_size and cuts[j] <= num):
                    j = j + 1
                sax.append(self.idx2letter(j-1))
        return ''.join(sax)
    
    def idx2letter(self, idx):
        if 0 <= idx < 25:
            return chr(97 + idx)
        else:
            raise ValueError('A wrong idx value supplied.')

    def generate_string_from_time_series(self, file_path_to_ts, letter_boundary_size, horizontal_window_size):
        data = self.generate(file_path_to_ts)
        return self.build_string_from_numpy_data(data, letter_boundary_size, horizontal_window_size)
    
    def build_string_from_numpy_data(self, data, letter_boundary_size, horizontal_window_size):
        windowed_data = self.apply_letter_window(data, horizontal_window_size)
        norm_data = self.normalise_data(windowed_data)
        options = norm_letter_conversion(letter_boundary_size)
        sax_string = self.ts_to_string(norm_data, options)
        return sax_string