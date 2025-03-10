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
PLOT_START_DATE = '2022-05-01'
PLOT_END_DATE   = '2022-11-01'

PERIOD_START_DATE = '2022-06-10'
PERIOD_END_DATE   = '2022-10-01'

MA_WINDOW = 7

# %%
reference_df = pd.read_pickle("D:/OneDrive - HKUST/LongCOVIDCode/data/msv/.g.11qm6vy88k.pkl")
ref_ma_df = reference_df.copy().rolling(MA_WINDOW).mean()

reference_df = reference_df.query(f'date >= \'{PLOT_START_DATE}\' & date <= \'{PLOT_END_DATE}\'')
ref_ma_df = ref_ma_df.query(f'date >= \'{PLOT_START_DATE}\' & date <= \'{PLOT_END_DATE}\'')

reference_df = reference_df.reset_index()
ref_ma_df = ref_ma_df.reset_index()

# %%
print(f"{len(keyword_query_results)=}")

if True:
# with PdfPages('./graphs/20240423-LongCV-MSVs.1st.pdf') as pdf:
    for index, tag in enumerate(keyword_query_results[1:]):
        keyword = new_labels[tag].strip()

        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 6))
        plt.title(f'{keyword} ({tag})')
    
        ax2 = ax1.twinx()
        escaped_tag = tag.replace("/", ".")

        msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_tag}.pkl")
        
        # Create MA dataframe
        msv_ma_df = msv_df.copy().rolling(MA_WINDOW).mean()
        msv_ma_df = msv_ma_df.query(f'date >= \'{PLOT_START_DATE}\' & date <= \'{PLOT_END_DATE}\'').reset_index()
        
        msv_df = msv_df.query(f'date >= \'{PLOT_START_DATE}\' & date <= \'{PLOT_END_DATE}\'').reset_index()
        
        
        # Calculate MA-Data Maxima
        sort_ma_df = msv_ma_df.copy()
        sort_ma_df.sort_values(by=['msv'], ascending=False, inplace=True)
        max_ma_date = sort_ma_df['date'].iloc[0]
        
        # Calculate Data Maxima
        sort_orig_df = msv_df.copy().query(f'date >= \'{PERIOD_START_DATE}\' & date <= \'{PERIOD_END_DATE}\'').reset_index()
        sort_orig_df.sort_values(by=['msv'], ascending=False, inplace=True)
        max_orig_date = sort_orig_df['date'].iloc[0]
        
        # Calculate Ref Maxima
        sort_ref_df = reference_df.query(f'date >= \'{PERIOD_START_DATE}\' & date <= \'{PERIOD_END_DATE}\'').reset_index()
        sort_ref_df.sort_values(by=['msv'], ascending=False, inplace=True)
        max_ref_date = sort_ref_df['date'].iloc[0]
        
        # Calculate Ref-MA Maxima
        sort_ref_df = ref_ma_df.query(f'date >= \'{PERIOD_START_DATE}\' & date <= \'{PERIOD_END_DATE}\'').reset_index()
        sort_ref_df.sort_values(by=['msv'], ascending=False, inplace=True)
        max_refma_date = sort_ref_df['date'].iloc[0]
                

        """
         Draw plot
        """

        # Draw wave period
        plt.axvspan(
            date.fromisoformat(PERIOD_START_DATE), 
            date.fromisoformat(PERIOD_END_DATE), 
            color='tab:green',
            alpha=0.3
        )

        # Draw line plots
        ax1.plot('date', 'msv', data=msv_df, label=keyword, color='tab:blue', linewidth=1.15, alpha=0.65)
        ax1.plot('date', 'msv', data=msv_ma_df, label=keyword + f"[MA({MA_WINDOW})]", color='blue', linewidth=1.5, alpha=1)
        ax2.plot('date', 'msv', data=reference_df, label="Long COVID (reference)", color='darkgray', linewidth=1.15, alpha=0.65)
        ax2.plot('date', 'msv', data=ref_ma_df, label=f"Long COVID (reference)[MA({MA_WINDOW})]", color='black', linewidth=1.5, alpha=1)
        
        # Draw lines 
        plt.axvline(
            x=max_orig_date,
            color='tab:blue',
            linestyle=":"
        )
        
        plt.axvline(
            x=max_ref_date,
            color='black',
            linestyle=":"
        )
        
        # plt.axvline(
        #     x=max_ma_date,
        #     color="tab:blue",
        #     linestyle="--"
        # )
        
        # plt.axvline(
        #     x=max_refma_date,
        #     color="black",
        #     linestyle="--"
        # )

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
        

        ax1.set_xlim(left=date.fromisoformat(PLOT_START_DATE), right=date.fromisoformat(PLOT_END_DATE))
        plt.tight_layout()

        # pdf.savefig()  # saves the current figure into a pdf page
        plt.savefig('d://OneDrive - HKUST//LongCOVIDCode//graphs//MSVPair-2ndWave//' + keyword + ".png")
        plt.savefig('d://OneDrive - HKUST//LongCOVIDCode//graphs//MSVPair-2ndWave//' + keyword + ".pdf")
        plt.close()


# plt.savefig('./graphs/20231110-LongCV-MSVs.pdf', bbox_inches='tight')
# plt.show()
# %%
