# %%
from os.path import abspath

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

# %%
df = pd.read_pickle(abspath('./data/msv/joined_msvs.pkl'))

# %%
# plt.rcParams.update({'font.size': 12})

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection="polar")

# %%
for header in df.columns:
    radius = df[header].values
    angle = np.linspace(start=0, stop=2 * np.pi, num=len(df))

    radius = np.append(radius, radius[0])
    angle = np.append(angle, angle[0])

    ax.plot(angle, radius, lw=1, alpha=.75, label=header)

# %%

ax.set_xticks(
    ticks=np.linspace(0, 2 * np.pi, num=4 + 1),
    labels=["", r"$\frac{1}{2} \pi$", "$\\pi$", r"$\frac{3}{2} \pi$", "$2\\pi$"],
)
ax.xaxis.set_tick_params(
    labelsize=22,
)

ax.yaxis.set_major_locator(MultipleLocator(4000))
ax.yaxis.set_tick_params(which='major', width=4, labelsize=10)
plt.grid(axis='y', which='major', color='black', linestyle='-')

ax.yaxis.set_minor_locator(MultipleLocator(2000))
ax.yaxis.set_tick_params(which='minor', width=2, labelsize=10)
plt.grid(axis='y', which='minor', color='grey', linestyle=':')

plt.savefig('graphs/20231109-UnscaledPolarProjection.pdf', bbox_inches=None)
plt.savefig('graphs/20231109-UnscaledPolarProjection.png', bbox_inches=None)
plt.show()