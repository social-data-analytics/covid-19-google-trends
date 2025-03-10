# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")
# %%
from mongo.get_database import get_database
import pickle
from datetime import datetime

# %%
db = get_database()
collection = db.get_collection('jobs')


# %%
# filter = {}

# if len(sys.argv) > 1:
#     filter = {
#         '_id': sys.argv[1],
#     }
# else:
#     id = input("Please enter a document ID: ")
#     filter = {
#         '_id': id,
#         # 'keyword': '/m/013677',
#         # 'end_date': {
#         #     '$gte': datetime.fromisoformat('2021-04-08 00:00:00'),
#         #     '$lt': datetime.fromisoformat('2021-04-08 23:59:59'),
#         # },
#         # 'downloaded': {
#         #     '$type': 'binData'
#         # }
#     }

# %%
for id in ['width_29d_.m.03l19k_20220522',
'width_29d_.m.03l19k_20220718',
'width_29d_.m.03l19k_20220829',
'width_29d_.m.03l19k_20220910',
'width_29d_.m.03l19k_20230114']:
    filter = {'_id': id}
    document = collection.find_one(filter=filter)
    assert document is not None, 'No doucment found.'

    # id = document.get('_id')
    df = pickle.loads(document.get('downloaded'))
    df.columns = ['downloaded']

    old_downloaded = pickle.loads(document.get('old_downloaded'))
    old_downloaded.columns = ['old_downloaded']
    df = df.join(old_downloaded, how='outer')

    incomplete_downloaded = pickle.loads(document.get('incomplete_downloaded'))
    incomplete_downloaded.columns = ['incomplete_downloaded']
    df = df.join(incomplete_downloaded, how='outer')

    # %%
    print(f"{id=}")
    print(f"{document.get('start_date')=}")
    print(f"{document.get('end_date')=}")
    print(df)
    print(f"{df.shape}")
    print('='*72)