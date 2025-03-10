# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
import numpy as np
import pandas as pd
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import matplotlib.dates as mdates
import seaborn as sns
from info.keywords import labels
from info.covid_events import covid_events

# %%

netstats_df = pd.read_csv('./data/netstats.csv', parse_dates=['date'])
S_t_df = pd.read_pickle('./data/s_t/vary_thresholds.pkl')

# %%
fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(10, 5))
# plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.08, wspace=0.45)

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.967,
                    top=0.97,
                    wspace=0.3,
                    hspace=0.1)
g = sns.lineplot(data=S_t_df,
            x='date', y='S_t', hue='threshold', palette="viridis")

for covid_events_date in [date.fromisoformat(covid_event) for covid_event in covid_events.keys()]:
    plt.axvline(x=covid_events_date, linestyle=":")
# ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha='right')

plt.savefig('./graphs/20230618-LongCV-S-t.pdf')
# plt.show()
plt.close()

fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(10, 5))
# plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.08, wspace=0.45)

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.967,
                    top=0.97,
                    wspace=0.3,
                    hspace=0.1)
g = sns.lineplot(data=S_t_df.query('threshold == 0.5'),
            x='date', y='S_t', color="#21918c")

ax2 = axs.twinx()

sns.lineplot(data=netstats_df, x='date', y='density', ax=ax2)

for covid_events_date in [date.fromisoformat(covid_event) for covid_event in covid_events.keys()]:
    plt.axvline(x=covid_events_date, linestyle=":")
# ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha='right')

plt.savefig('./graphs/20230619-LongCV-St-vs-NetDensity.pdf')
exit(0)


fig, axs = plt.subplots(nrows=6, ncols=4, sharex=True, figsize=(15, 10))
fig.tight_layout(pad=5)
plt.subplots_adjust(left=0.07,
                    bottom=0.08,
                    right=1-0.07,
                    top=0.97,
                    wspace=0.3,
                    hspace=0.1)

for index, tag in enumerate(tags):
    print(index, tag)
    sub_df = S_t_df.query(f'tag == "{tag}"')
    
    col_number = index % 4
    row_number = int(index / 4)
    ax = axs[row_number, col_number]

    if index == 0:
        g = sns.lineplot(x='date', y='value', hue='threshold',
                         data=sub_df,
                         ax=ax, label="Local clustering coefficient")
    else:
        g = sns.lineplot(x='date', y='value', hue='threshold',
                         data=sub_df,
                         ax=ax)
    ax.get_legend().remove()
    g.set(yticks=[])

    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())

    ax.set_ylabel(labels[tag])
    ax.set_xlabel(None)

    # ax.get_legend().remove()
    # ax2.get_legend().remove()

for col_number in range(4):
    ax = axs[5, col_number]
    ax.set_yticks([])
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=45, ha='right')

fig.delaxes(axs[5][2])
fig.delaxes(axs[5][3])

# fig.legend(loc='lower right')
plt.savefig('./graphs/20230612-LongCV-LocalCC.pdf', bbox_inches='tight')
plt.show()
