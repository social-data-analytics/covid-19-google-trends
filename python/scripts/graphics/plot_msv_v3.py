# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
import math
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.dates import MonthLocator
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

from pymongo import MongoClient
from info.keywords import labels, new_labels

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

keyword_query_results = list(new_labels.keys())

# %%
print(f"{len(keyword_query_results)=}")

with PdfPages('./graphs/20240402-LongCV-MSVs.pdf') as pdf:
    for index, tag in enumerate(keyword_query_results):
        keyword = new_labels[tag].strip()

        plt.figure(figsize=(5, 3))
        plt.title(f'{keyword} ({tag})')
        plt.tight_layout()
        plt.subplots_adjust(
            top=0.98,
            bottom=0.15,
            left=0.15,
            right=0.99,
            hspace=0.1,
            wspace=0.015
        )
        
        escaped_tag = tag.replace("/", ".")

        msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_tag}.pkl")
        msv_df = msv_df[msv_df.index.date >= date.fromisoformat('2022-01-01')]
        sns.lineplot(x="date", y="msv", data=msv_df)

        plt.gca().set_title("")
        # plt.gca().tick_params(labelrotation=90)
        plt.gca().set_xlabel("")
        plt.gca().set_ylabel(keyword)

        plt.gca().xaxis.set_major_locator(MonthLocator(bymonth=[1]))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        plt.gca().xaxis.set_minor_locator(MonthLocator(bymonth=[4, 7, 10]))
        plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
        
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(4))
        plt.gca().yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, p: format(int(x), ','))
        )

        pdf.savefig()  # saves the current figure into a pdf page
        if index == 1:
            plt.show()

        plt.close()


# plt.savefig('./graphs/20231110-LongCV-MSVs.pdf', bbox_inches='tight')
# plt.show()