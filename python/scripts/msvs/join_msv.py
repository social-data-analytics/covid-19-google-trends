# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")
# %%
import os
import pandas as pd
import pickle
from mongo.get_database import get_database
from info.keywords import labels

# %% Establish connection to MongoDB
db = get_database()
msv_collection = db.get_collection('msvs')

full_msv_df_csv_path = os.path.abspath('./data/msv/joined_msvs.csv')
full_msv_df_pkl_path = os.path.abspath('./data/msv/joined_msvs.pkl')

# %% Combine every MSV into a dataframe
msv_documents = msv_collection.find(filter={
    'keyword': {
        '$in': list(labels.keys())
    },
    'duration': 29,
})

full_df = None

for msv_document in msv_documents:
    keyword = msv_document.get('keyword')
    msv_df = pickle.loads(msv_document.get('msv'))
    msv_df.rename(columns={'msv': keyword}, inplace=True)

    if full_df is None:
        full_df = msv_df.copy()
    else:
        full_df = full_df.join(msv_df, how='outer')
        print(f"{keyword=}")
        print(f"{full_df.shape=}")
        pd.set_option('display.max_columns', None)
        print(full_df.tail())

full_df.to_csv(full_msv_df_csv_path)
full_df.to_pickle(full_msv_df_pkl_path)

print(f"{full_df.shape=}")