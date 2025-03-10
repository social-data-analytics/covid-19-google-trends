# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")
# %%
from mongo.get_database import get_database
import pickle
# import pandas as pd
from mongo.filters_and_aggregators import find_downloaded_rsvs, find_old_downloaded_rsvs

# %%

# %%
db = get_database()
collection = db.get_collection('jobs')

# %%
documents = collection.find(filter={
    'downloaded': {
        '$type': 'binData',
    }
})

for index, rsv_data in enumerate(documents):
    id = rsv_data.get('_id')
    keyword = rsv_data.get('keyword')
    # start_date = rsv_data.get('start_date')
    # end_date = rsv_data.get('end_date')
    rsv_binary = rsv_data.get('downloaded')
    rsv_binary_length = len(rsv_binary)

    print('[info]', f"Handling document ID: {id}, binary length: {rsv_binary_length}")

    if rsv_binary_length == 0:
        print('[warn]', f"Document ID: {id} has an empty binary. Re-queue...")
        collection.update_one(
            filter={
                '_id': id
            },
            update={
                '$set': {
                    'downloaded': False
                }
            }
        )
        continue

    df = pickle.loads(rsv_binary)
    print('[info]', id, df.shape)

    if not df.columns[0] == keyword:
        print('[erro]', f"Document ID: {id} has an incorrect RSV.", 'Expected:', keyword, 'Found:', df.columns[0])
        collection.update_one(
            filter={
                '_id': id
            },
            update={
                '$rename': {
                    'downloaded': 'incorrect_downloaded'
                }
            }
        )

        collection.update_one(
            filter={
                '_id': id
            },
            update={
                '$set': {
                    'downloaded': False
                }
            }
        )

    # if df.shape[0] < 30:
        # print("!!!!!" if df.shape[0] < 30 else "     ",
                #   id, keyword, start_date, end_date, df.shape)
    
    collection.update_one(
        filter={
            '_id': id
        },
        update={
            '$set': {
                'duration': df.shape[0]
            }
        }
    )

# %%
# data = collection.update_many(
#     filter={"old_downloaded": {"$type": "binData"}},
#     update={"$set": {"downloaded": False}}
# )
# print(f"{data=}")