# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from info.keywords import labels

# %%
msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/joined_msvs.pkl")
msv_df = msv_df.reset_index()
diff_df = msv_df.copy()

diff_df.iloc[:, 1:] = msv_df.iloc[:, 1:].pow(0.5).diff(periods=1, axis=0)

# %%
diff_df_ma = diff_df.copy()
diff_df.to_csv('temp.diff_df.csv')
diff_df_ma.iloc[:, 1:] = diff_df_ma.iloc[:, 1:].rolling(7).mean()
diff_df_ma.to_csv('temp.diff_df_ma.csv')

diff_df_ma = diff_df_ma.query('date >= "2022-01-01"')
print(diff_df_ma.head(3))

melt_df = pd.melt(diff_df, id_vars=['date'], var_name='tag', value_name='msv')
print(f"{melt_df['tag'].values=}")
melt_df['label'] = [ labels[tag].strip().replace("\n", "") for tag in melt_df['tag'] ]

reference_df = melt_df.query("tag == '/g/11qm6vy88k'")
melt_df = melt_df.query("tag != '/g/11qm6vy88k'")

list_of_tags = list(labels.keys())
list_of_tags.remove('/g/11qm6vy88k')




# %%
fig, ax = plt.subplots(nrows=6, ncols=4, figsize=(15,8), sharex=True)

# # %%
# top_right_ax = fig.subplot2grid((1, 3), (0, 3), colspan=3)
# sns.lineplot(data=reference_df,
#                  x='date', y='msv', color="tab:orange", alpha=0.6,
#                  ax=top_right_ax)

# %%
for index, tag in enumerate(list_of_tags):
    current_index = index + 1
    col_index = current_index % 4
    row_index = int(current_index / 4)

    print(row_index, col_index, tag)

    left_ax = ax[row_index][col_index]
    right_ax = left_ax.twinx()

    sns.lineplot(data=reference_df,
                 x='date', y='msv', color="orange", alpha=0.6,
                 ax=right_ax)
    sns.lineplot(data=melt_df.query(f'tag == \'{tag}\''),
                 x='date', y='msv', color="tab:blue", alpha=0.9, 
                 ax=left_ax, label=labels[tag].replace("\n", "").replace(" (", "\n(").strip())
    
    left_ax.set_yticks([])
    left_ax.set_ylabel('')
    right_ax.set_yticks([])
    right_ax.set_ylabel('')

    left_ax.legend(loc='lower left')

    left_ax.xaxis.set_tick_params(which='major', labelrotation=90)

# %%
# %%
sns.lineplot(data=reference_df,
    x='date', y='msv', color="tab:orange",
    ax=ax[0][0], label="Long COVID (Reference,\nMA(7) smoothed)",
)
ax[0][0].set_yticks([])

# %%
fig.delaxes(ax[5][2])
fig.delaxes(ax[5][3])

# %%
# Modify x-tick
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

plt.gca().xaxis.set_tick_params(which='major', labelrotation=90)

fig.subplots_adjust(
    top=0.99,
    bottom=0.065,
    left=0.005,
    right=0.995,
    hspace=0.0,
    wspace=0.0
)
plt.show()
