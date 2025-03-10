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

keyword_query_results = list(labels.keys())

# START_DATE = "2022-06-10"

reference_df = pd.read_pickle("D:/OneDrive - HKUST/LongCOVIDCode/data/msv/.g.11qm6vy88k.pkl").reset_index()

# %%
print(f"{len(keyword_query_results)=}")

if True:
# with PdfPages('./graphs/20240423-LongCV-MSVs.1st.pdf') as pdf:
    for index, tag in enumerate(keyword_query_results[1:]):
        keyword = new_labels[tag].strip()

        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5, 4))
        plt.title(f'{keyword} ({tag})')
    
        ax2 = ax1.twinx()
        escaped_tag = tag.replace("/", ".")

        msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_tag}.pkl")
        msv_df = msv_df.reset_index()

        # data_df = pd.concat([msv_df, reference_df], axis=1, join='outer').reset_index()
        # data_df = data_df.set_axis(['date', 'keyword', 'reference'], axis=1).melt(id_vars='date',value_vars=['keyword', 'reference'], var_name='type', value_name='msv')

        ax1.plot('date', 'msv', data=msv_df, label=keyword, color='tab:blue')
        ax2.plot('date', 'msv', data=reference_df, label="Long COVID (reference)", color='grey', alpha=0.75)
        # sns.lineplot(x="date", y=["msv_x", "msv_y"], data=data_df, color="tab:blue", ax=ax1, label=keyword)
        # sns.lineplot(x="date", y="msv", data=reference_df, color="tab:grey", ax=ax2, alpha=0.75, label="Long COVID")

        fig.legend(framealpha=1)

        ax1.set_title("")
        ax1.set_xlabel("")
        ax1.set_ylabel(keyword.replace("\n", ""))

        ax1.xaxis.set_major_locator(MonthLocator(bymonth=[1]))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        ax1.xaxis.set_minor_locator(MonthLocator())
        ax1.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))
        
        ax2.tick_params(labelrotation=90)
        ax2.set_ylabel("Long COVID (Reference)")
        ax2.yaxis.set_major_locator(plt.MaxNLocator(4))
        ax2.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, p: format(int(x), ','))
        )

        plt.axvspan(
            date.fromisoformat('2021-11-20'), 
            date.fromisoformat('2022-02-06'), 
            color='tab:orange',
            alpha=0.1
        )
        
        plt.axvspan(
            date.fromisoformat('2022-06-10'), 
            date.fromisoformat('2022-10-01'), 
            color='tab:green',
            alpha=0.1
        )

        ax1.set_xlim(left=date.fromisoformat('2020-01-01'), right=date.fromisoformat('2023-12-31'))
        plt.tight_layout()

        # pdf.savefig()  # saves the current figure into a pdf page
        plt.savefig('d://OneDrive - HKUST//LongCOVIDCode//graphs//MSVPair-2waves//' + keyword + ".png")
        plt.savefig('d://OneDrive - HKUST//LongCOVIDCode//graphs//MSVPair-2waves//' + keyword + ".pdf")
        plt.close()


# plt.savefig('./graphs/20231110-LongCV-MSVs.pdf', bbox_inches='tight')
# plt.show()
# %%
