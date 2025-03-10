# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from os.path import abspath

# %%
netstats_df = pd.read_pickle(abspath('./data/network_stats.pkl'))
print(netstats_df.head())

# %%
netstats = ('density', 'transitivity', 'assortativity')
netstats_label = ('Network Density', 'Clustering Coefficient', 'Assortativity')

fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 8))

for index, stat_item in enumerate(netstats):

    sns.lineplot(x="date", y=stat_item, data=netstats_df, ax=ax[index])

    ax[index].set_ylabel(netstats_label[index])

plt.savefig('./graphs/LongCV-Netstats.pdf', bbox_inches='tight')
plt.show()