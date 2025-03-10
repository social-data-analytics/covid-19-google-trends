# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from info.keywords import labels

_MA_FACTOR = 0

# %%
msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/joined_msvs.pkl")
msv_df = msv_df.reset_index()
diff_df = msv_df.copy()

# diff_df.iloc[:, 1:] = msv_df.iloc[:, 1:].pow(0.5).diff(periods=1, axis=0)

if _MA_FACTOR > 0:
    diff_df.iloc[:, 1:] = diff_df.iloc[:, 1:].rolling(_MA_FACTOR).mean()

# Date selectopm
diff_df = diff_df.query('date >= "2020-01-01"')
# diff_df = diff_df.query('date >= "2021-01-15"')

melt_df = pd.melt(diff_df, id_vars=['date'], var_name='tag', value_name='msv')
print(f"{melt_df['tag'].values=}")
melt_df['label'] = [ labels[tag].strip().replace("\n", "") for tag in melt_df['tag'] ]

reference_df = melt_df.query("tag == '/g/11qm6vy88k'")
melt_df = melt_df.query("tag != '/g/11qm6vy88k'")

list_of_tags = list(labels.keys())
list_of_tags.remove('/g/11qm6vy88k')


# %%
fig, ax = plt.subplots(nrows=6, ncols=4, figsize=(15,8), sharex=False)
for index, tag in enumerate(list_of_tags):
    current_index = index
    col_index = current_index % 4
    row_index = int(current_index / 4)

    print(row_index, col_index, tag)

    left_ax = ax[row_index][col_index]
    right_ax = left_ax.twinx()

    sns.lineplot(data=reference_df,
                 x='date', y='msv', color="tab:blue", 
                 ax=left_ax)
    sns.lineplot(data=melt_df.query(f'tag == \'{tag}\''),
                 x='date', y='msv', color="tab:grey", 
                 alpha=0.8, 
                 ax=right_ax, label=labels[tag].replace("\n", "").strip())
    
    left_ax.set_xlabel('')
    right_ax.set_xlabel('')

    left_ax.set_yticks([])
    left_ax.set_ylabel('')
    right_ax.set_yticks([])
    right_ax.set_ylabel('')

    # right_ax.legend(loc='lower right')

    left_ax.xaxis.set_tick_params(which='major', labelrotation=90)

    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
    plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

# # %%
# # Draw 21 other lines
# g = sns.FacetGrid(melt_df, col='label', hue='label',
#                   col_wrap=4, legend_out=False,
#                   sharex=True, sharey=False, despine=True)

# # %%
# # Draw left: keyword lines
# def draw_left_axes(data, label, **kwargs):
#     left_ax = plt.gca()
#     sns.lineplot(data=data,
#                 x="date", y="msv", alpha=0.9, label=label, 
#                 palette="deep", hue='label',
#                 ax=left_ax)

#     left_ax.set_yticks([])
#     left_ax.set_ylabel('')

# # %%
# # Draw right: "Long COVID" line
# def draw_right_axes(**kwargs):
#     right_ax = plt.twinx()
#     sns.lineplot(data=reference_df, 
#                  x='date', y='msv', color="grey", alpha=0.9,
#                  ax=right_ax)
    
#     right_ax.set_yticks([])
#     right_ax.set_ylabel('')

# g.map_dataframe(draw_left_axes, label='label')
# g.map(draw_right_axes)
# g.add_legend()

# g.set_titles('')
# g.set_axis_labels(x_var='', y_var='')

# %%
# sns.lineplot(data=reference_df,
#     x='date', y='msv', color="tab:orange",
#     ax=ax[0][0], label=f"Long COVID\n(Reference, MA({_MA_FACTOR}))" if _MA_FACTOR > 0 else "Long COVID\n(Reference)",
# )
ax[0][0].set_yticks([])

fig.delaxes(ax[5][1])
fig.delaxes(ax[5][2])
fig.delaxes(ax[5][3])


plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

fig.subplots_adjust(
    top=0.99,
    bottom=0.065,
    left=0.005,
    right=0.995,
    hspace=0.0,
    wspace=0.0
)

plt.savefig(f"./graphs/20231115-LCV-MSV-LongCOVID-vs-otherKeywords-MA({_MA_FACTOR}).pdf")
plt.savefig(f"./graphs/20231115-LCV-MSV-LongCOVID-vs-otherKeywords-MA({_MA_FACTOR}).png")
plt.show()
