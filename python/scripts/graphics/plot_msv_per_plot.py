# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.dates import MonthLocator
from matplotlib.backends.backend_pdf import PdfPages
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

reference_df = pd.read_pickle("D:/OneDrive - HKUST/LongCOVIDCode/data/msv/.g.11qm6vy88k.pkl").query('date >= \'2021-11-01\'')

# %%
print(f"{len(keyword_query_results)=}")

with PdfPages('./graphs/20240222-LongCV-MSVs.pdf') as pdf:
    for index, tag in enumerate(keyword_query_results[1:]):
        keyword = labels[tag].strip()
        linebreaks = keyword.count("\n")

        if linebreaks < 2:
            keyword += "\n" * (2 - linebreaks)

        print(index, tag, keyword)

        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5, 4))
        plt.title(f'{keyword} ({tag})')

    
        ax2 = ax1.twinx()
        escaped_tag = tag.replace("/", ".")

        msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_tag}.pkl")
        print(msv_df.head())
        msv_df = msv_df.query('date >= \'2021-11-01\'')

        sns.lineplot(x="date", y="msv", data=msv_df, color="tab:blue", ax=ax1,)
        sns.lineplot(x="date", y="msv", data=reference_df, color="tab:grey", ax=ax2, alpha=0.65,)

        ax1.set_title("")
        ax1.tick_params(labelrotation=90)
        ax1.set_xlabel("")
        ax1.set_ylabel(keyword.replace("\n", ""))

        ax1.xaxis.set_major_locator(MonthLocator(bymonth=[1]))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax1.xaxis.set_minor_locator(MonthLocator(bymonth=[4, 7, 10]))
        ax1.xaxis.set_minor_formatter(mdates.DateFormatter("%B"))
        
        ax2.tick_params(labelrotation=90)
        ax2.set_ylabel("Long COVID\n(Reference, Grey)")
        ax2.yaxis.set_major_locator(plt.MaxNLocator(4))
        ax2.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, p: format(int(x), ','))
        )

        ax1.set_xlim(left=date.fromisoformat('2021-11-01'), right=date.fromisoformat('2023-12-31'))

        # if index == 17:
        #     plt.show()

        plt.tight_layout()

        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()


# plt.savefig('./graphs/20231110-LongCV-MSVs.pdf', bbox_inches='tight')
# plt.show()