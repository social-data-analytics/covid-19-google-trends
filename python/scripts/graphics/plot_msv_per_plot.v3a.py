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

# %%
PLOT_START_DATE = '2021-11-01'
PLOT_END_DATE   = '2022-02-25'

PERIOD_START_DATE = '2021-11-20'
PERIOD_END_DATE   = '2022-02-06'

reference_df = pd.read_pickle("D:/OneDrive - HKUST/LongCOVIDCode/data/msv/.g.11qm6vy88k.pkl").query(f'date >= \'{PLOT_START_DATE}\' & date <= \'{PLOT_END_DATE}\'').reset_index()

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
        msv_df = msv_df.query(f'date >= \'{PLOT_START_DATE}\'').reset_index()

        ax1.plot('date', 'msv', data=msv_df, label=keyword, color='tab:blue')
        ax2.plot('date', 'msv', data=reference_df, label="Long COVID (reference)", color='grey', alpha=0.75)

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
            date.fromisoformat(PERIOD_START_DATE), 
            date.fromisoformat(PERIOD_END_DATE), 
            color='tab:orange',
            alpha=0.15
        )

        ax1.set_xlim(left=date.fromisoformat(PLOT_START_DATE), right=date.fromisoformat(PLOT_END_DATE))
        plt.tight_layout()

        # pdf.savefig()  # saves the current figure into a pdf page
        plt.savefig('d://OneDrive - HKUST//LongCOVIDCode//graphs//MSVPair-1stWave//' + keyword + ".png")
        plt.savefig('d://OneDrive - HKUST//LongCOVIDCode//graphs//MSVPair-1stWave//' + keyword + ".pdf")
        plt.close()


# plt.savefig('./graphs/20231110-LongCV-MSVs.pdf', bbox_inches='tight')
# plt.show()