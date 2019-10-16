import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import cm
import joypy

import pandas as pd
import numpy as np

# Import dataframe
df_col = pd.read_csv("logP_submission_collection.csv", index_col=[0])
print(df_col.head())

# Make ridge plot
fig, axes = joypy.joyplot(df_col, by = "Molecule ID", column = "$\Delta$logP error (calc - exp)", figsize=(3, 6),
                          colormap=cm.plasma)
axes[-1].set_xlabel("logP error (calc - exp)")
plt.savefig("ridge.pdf")