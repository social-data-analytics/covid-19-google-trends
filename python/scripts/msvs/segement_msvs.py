# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

# %%
from mongo.get_database import get_database
import pickle
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
from info.keywords import labels

logging.basicConfig(level=logging.INFO)

# %%
db = get_database()
segmented_msv_collection = db.get_collection('segmented_msvs')

# %% Read Joined MSV dataframe
full_msv_df_pkl_path = os.path.abspath('./data/msv/joined_msvs.pkl')
full_msv_df = pd.read_pickle(full_msv_df_pkl_path)
print(f"{full_msv_df.shape=}")

# # %%
# certain_duration_only_pipeline = {
#     "$match": {
#         "duration": {
#             "$eq": 29
#         },
#         "keyword": {
#             "$in": list(labels.keys())
#         }
#     }
# }

# msvs = list(msv_collection.aggregate(
#     pipeline=[certain_duration_only_pipeline]))

# %% Segment MSVs
for index in range(len(full_msv_df) - 29 + 1):
    sub_df = full_msv_df.iloc[index:index+29, ].copy()

    print('[i]', f"{len(sub_df.columns)=}")
    print(sub_df.columns)

    start_date = sub_df.index[0]
    end_date = sub_df.index[-1]
    print('[i]', 'segmenting msvs from', start_date, end_date)

    segmented_msv_pickle_path = './temp-segmented-msvs.pkl'
    sub_df.to_pickle(segmented_msv_pickle_path)

    id = start_date.strftime("%Y%m%d") + "_" + \
         end_date.strftime("%Y%m%d") + "_" + \
         str(sub_df.shape[0]) + "x" + \
         str(sub_df.shape[1])
    
    f = open(segmented_msv_pickle_path, "rb")

    segmented_msv_collection.update_one({"_id": {"$eq": id}}, {"$set": {
        "_id": id,
        "msv": f.read(),
        "start_date": start_date,
        "end_date": end_date,
        "last_attempted": datetime.fromisoformat("1970-01-01"),
        "shape": sub_df.shape,
    }}, upsert=True)

    f.close()
