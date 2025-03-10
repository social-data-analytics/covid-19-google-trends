# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")
# %%
import numpy as np
import pandas as pd
import math
import pickle
from datetime import datetime
from mongo.get_database import get_database

# %% Establish connection to MongoDB
db = get_database()
rsv_collection = db.get_collection('jobs')
msv_collection = db.get_collection('msvs')

ignored_ids = []

# %%
# Find keyword list
find_keyword_pipeline = [
    {
        "$set": {
            "request_duration": {
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
            'keyword': {
                # '$in': list(labels.keys())
                '$in': [
                    '/m/0dl9s3k', 
                    # '/m/0j5fv', 
                    # '/m/01cdt5',
                ]
            },
            "request_duration": 29 - 1,
            "downloaded": {
                "$type": "binData"
            },
            "start_date": {
                "$gte": datetime.fromisoformat('2020-01-01T00:00:00Z')
            },
            "end_date": {
                "$lt": datetime.fromisoformat('2024-01-01T00:00:00Z')
            },
            "_id": {
                "$not": {
                    "$in": ignored_ids
                }
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
            },
            "series": {
                "$push": {
                    "_id": "$_id",
                    "start_date": "$start_date",
                    "end_date": "$end_date",
                    "rsv_series": "$downloaded"
                }
            }
        }
    },{
        "$sort": {
            "keyword": 1,
        }
    },
]

# width_29d_.g.11bytn80mf_20230406
keyword_query_results = list(
    rsv_collection.aggregate(pipeline=find_keyword_pipeline)
)

# %% # Debug only %%
# for keyword_item in keyword_query_results:
#     print(keyword_item.get('keyword'))
#     print(
#         "\n".join(
#             [
#                 "(%s, %s)" % (rsv.get('start_date').date, rsv.get('end_date').date)
#                 for rsv in keyword_item.get('series')
#             ]
#         )
#     )
# exit(0)

# %% Overwrite existing record
# f = open('.\zero_ids.txt', 'w')
# f.write('')
# f.close()

# %%
for keyword_item in keyword_query_results:
    keyword = keyword_item.get('keyword')
    escaped_keyword = keyword.replace("/", ".")
    series = keyword_item.get('series')

    print('[info]', keyword, len(series))
    # print('[info]', keyword, len(series))

    msv_df = pd.DataFrame()

    for data in keyword_item.get('series'):
        id         = data.get('_id')
        start_date = data.get('start_date').strftime("%Y-%m-%d")
        end_date =   data.get('end_date').strftime("%Y-%m-%d")
        rsv_pickle = data.get('rsv_series')
        rsv_df = pickle.loads(rsv_pickle)

        # print('[info]', 'Processing # %s' % id, start_date, end_date)

        if rsv_df.index.name is None:
            rsv_df.set_index('date', inplace=True)
            rsv_df = rsv_df.tz_localize(None)

        # if id.endswith("20230403") or id.endswith("20230404") or id.endswith("20230405"):
        #     print(rsv_df.index.name)
        #     print(rsv_df.head())

        luk_array = (rsv_df.index >= start_date) & (rsv_df.index <= end_date)
        rsv_df = rsv_df[luk_array]

        rsv_df.fillna(0, inplace=True)

        assert len(rsv_df) > 0, "RSV dataframe length must be larger than 0 at %s." % id
        if len(rsv_df) <= 0:
            rsv_collection.update_one({'_id': id}, {'$set': {'downloaded': False, 'df_length': 0}})
            rsv_collection.update_one({'_id': id}, {'$unset': {'df_length': ''}})
            continue

        if len(rsv_df) < 29:
            print('[warn]', f"Document (ID: {id}) has a length shorter than 29 days.", start_date, end_date, keyword, rsv_df.shape)

        if len(msv_df) <= 0:
            msv_df = rsv_df
        else:
            intersect_df = msv_df.join(
                rsv_df, how='inner', lsuffix='_x', rsuffix='_y')
            msv_df = msv_df.join(
                rsv_df, how='outer', lsuffix='_x', rsuffix='_y')
            intersect_df.columns = ['old', 'new']
            msv_df.columns = ['old', 'new']

            correction_factors = (intersect_df['old'] / intersect_df['new'])
            correction_factors = correction_factors.replace([np.inf, 0, -np.inf], 1).dropna()
            correction_factor = correction_factors.mean(skipna=True)
            
            # print('[info]', 'Document # %s has a correction factor of %.04f' % (id, correction_factor))
            print(id, ",", end_date, ",", "%.04f" % correction_factor, ',', len(rsv_df) - len(intersect_df))
            # print('[info]', 'tail of intersect_df:')
            # print("df extended by %d at %s" % (len(rsv_df) - len(intersect_df), id))

            assert len(rsv_df) - len(intersect_df) > 0, 'Dataframe did not extend at %s' % id
            assert correction_factor > 0, 'Correction factor hit 0 at %s.' % id

            if correction_factor <= 0 or rsv_df.shape[0] == 0:
                ignored_ids.append(id)

                f = open('.\ignored_ids.txt', 'a')
                f.write(id + '\n')
                f.close()

                # Record rewrite
                keyword_query_results = list(
                    rsv_collection.aggregate(pipeline=find_keyword_pipeline)
                )

                continue

            msv_df['corrected'] = msv_df['new'] * correction_factor
            msv_df['old'].fillna(msv_df['corrected'], inplace=True)

            if not msv_df['corrected'][-1] > 0:
                print('[warn]', 'Merged with 0 as result at ID %s.' % id)

                # f = open('.\zero_ids.txt', 'a')
                # f.write(id + '\n')
                # f.close()

            msv_df.drop(columns=['new', 'corrected'], inplace=True)
            # print("\n")

    print("[vvvv]", keyword, start_date, end_date, msv_df.shape)

    msv_df.index.name = 'date'
    msv_df.columns = ["msv"]

    msv_df.to_csv(
        f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_keyword}.csv", index=True)
    msv_df.to_pickle(
        f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_keyword}.pkl")


    data_id = f"{escaped_keyword}_29"
    with open(f"D:/OneDrive - HKUST/LongCOVIDCode/data/msv/{escaped_keyword}.pkl", "rb") as f:
        content = f.read()

        count = msv_collection.count_documents({"_id": data_id})
        print(f"{count=}")

        msv_collection.update_one(
            {"_id": data_id},
            {"$set":
                {
                     "_id": data_id,
                    "keyword": keyword,
                    "duration": 29,
                    "msv": content,
                    "start_date": msv_df.index[0],
                    "end_date": msv_df.index[-1],
                }
            },
            upsert=True
        )
