# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from info.keywords import labels

# %%
client = MongoClient("mongodb://localhost")
db = client['longcv']
collection = db.get_collection('jobs')

# %%
find_keyword_pipeline = [
    {
        "$set": {
            "duration": {
                "$dateDiff": {
                    "startDate": "$start_date",
                    "endDate": "$end_date",
                    "unit": "day"
                }
            }
        }
    },
    {
        "$match": {
            "duration": {
                "$lte": 29
            }
        }
    },
    {
        "$sort": {
            "keyword": 1,
            "start_date": 1
        }
    },
    {
        "$group": {
            "_id": "$keyword",
            "keyword": {
                "$first": "$keyword"
            }
        }
    }
]

keyword_query_results = list(labels.keys())

# %%
number_of_msvs = len(keyword_query_results)
print(f"{number_of_msvs=}")

fig, ax = plt.subplots(nrows=6, ncols=4, sharex=True, figsize=(15, 10))
fig.tight_layout(pad=5)
plt.subplots_adjust(left=0.07,
                    bottom=0.08,
                    right=1-0.07,
                    top=0.97,
                    wspace=0.4,
                    hspace=0.1)

# print([keyword_item.get('keyword') for keyword_item in keyword_query_results if not keyword_item.get('keyword') in labels.keys()])

for index, keyword in enumerate(keyword_query_results):
    ncol = index % 4
    nrow = math.floor(index / 4)
    current_ax = ax[nrow][ncol]

    print(index, nrow, ncol, keyword)

    escaped_keyword = keyword.replace("/", ".")

    msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_keyword}.pkl")
    sns.lineplot(x="date", y="msv", data=msv_df, ax=current_ax)

    current_ax.tick_params(labelrotation=45)
    current_ax.set_ylabel(labels[keyword])

# @TODO Remove hardcode removal
fig.delaxes(ax[5][2])
fig.delaxes(ax[5][3])
# fig.delaxes(ax[4][4])


plt.savefig('./graphs/20230612-LongCV-MSVs.pdf', bbox_inches='tight')
plt.show()