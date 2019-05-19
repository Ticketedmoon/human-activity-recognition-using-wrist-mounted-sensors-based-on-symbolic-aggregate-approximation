# Import matplotlib library
import matplotlib

# Import graphing tools and libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""
This class was used to compare and contrast each of the different classes that I would be 
training a machine learning model on. I wanted to understand the intricacies of the data
and understand how each class was different to each other class. This class can produce
a graph from each time-series and also can produce a graph containing all 4 classes simultaneously.
"""

# Load in data from PPG datasets (../../resources/exercise-datasets)
# Contains 15000+ rows, 2 columns.
walk_set = pd.read_csv("../../resources/exercise-datasets/Walk01.csv", skiprows=[1])
run_set = pd.read_csv("../../resources/exercise-datasets/Run01.csv", skiprows=[1])
slow_cycle_set = pd.read_csv("../../resources/exercise-datasets/LowResistanceBike01.csv", skiprows=[1])
fast_cycle_set = pd.read_csv("../../resources/exercise-datasets/HighResistanceBike01.csv", skiprows=[1])

x = walk_set['\'Elapsed time\'']

y1 = walk_set['\'wrist_ppg\'']
y2 = run_set['\'wrist_ppg\'']
y3 = slow_cycle_set['\'wrist_ppg\'']
y4 = fast_cycle_set['\'wrist_ppg\'']

fig, ax = plt.subplots(ncols=1, nrows=1)

ax.plot(x, y1, x, y2, x, y3, x, y4)
ax.grid(linestyle='--')

start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, 75))

start, end = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(start, end, 1000))

plt.ylabel('mV')
plt.xlabel('Time (Milliseconds)')

plt.show()
