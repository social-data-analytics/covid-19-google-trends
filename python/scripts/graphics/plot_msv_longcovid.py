# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
from datetime import date
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter


# %%
plt.figure(figsize=(15, 4))
msv_df = pd.read_pickle(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/.g.11qm6vy88k.pkl")

msv_ma7_df = msv_df.rolling(7).mean()[7:]
msv_ma14_df = msv_df.rolling(14).mean()[14:]

sns.lineplot(x="date", y="msv", data=msv_df, label="Long COVID\n(Reference)")
# sns.lineplot(x="date", y="msv", data=msv_ma7_df, alpha=0.75)
# sns.lineplot(x="date", y="msv", data=msv_ma14_df, alpha=1)

plt.axvspan(
    date.fromisoformat('2021-11-20'), 
    date.fromisoformat('2022-02-06'), 
    color='tab:orange',
    alpha=0.3
)

plt.axvspan(
    date.fromisoformat('2022-06-10'), 
    date.fromisoformat('2022-10-01'), 
    color='tab:green',
    alpha=0.3
)

plt.gca().set_title("")
plt.gca().tick_params(labelrotation=90)
plt.gca().set_xlabel("")
plt.gca().set_ylabel("MSV")

plt.gca().tick_params(top=True, labeltop=True, bottom=False, labelbottom=False, which='both')
plt.gca().xaxis.set_major_locator(MonthLocator(bymonth=[1]))
plt.gca().xaxis.set_major_formatter(DateFormatter("%Y"))
plt.gca().xaxis.set_minor_locator(MonthLocator(bymonth=[4, 7, 10]))
plt.gca().xaxis.set_minor_formatter(DateFormatter("%B"))
plt.gca().set_xlim(
    left =date.fromisoformat('2020-01-01'), 
    right=date.fromisoformat('2023-12-31'),
)

        
plt.gca().yaxis.set_major_locator(plt.MaxNLocator(4))
plt.gca().yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, p: format(int(x), ','))
)
plt.tight_layout()

plt.savefig(f'./graphs/20231121-MSV-of-LongCOVID.pdf')
plt.savefig(f'./graphs/20231121-MSV-of-LongCOVID.png')

plt.show()