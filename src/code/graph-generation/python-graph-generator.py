# Import matplotlib library
import matplotlib

# Switch backend from tkinter to agg
matplotlib.use('agg')

# Import graphing tools and libraries
import matplotlib.pyplot as plt
plt.style.use('classic')

import pandas as pd
import numpy as np
import seaborn as sns
sns.set()

# Load in data from PPG datasets (../../resources/exercise-datasets)
# Contains 15000+ rows, 2 columns.
fmri = sns.load_dataset("fmri")
ax = sns.lineplot(x="time", y="wrist_ppg", data=fmri)

