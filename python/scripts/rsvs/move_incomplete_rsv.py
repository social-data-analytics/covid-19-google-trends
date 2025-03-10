# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")
# %%
from mongo.get_database import get_database

# %%
db = get_database()
collection = db.get_collection('jobs')

# %%
job_id = None
if len(sys.argv) > 1:
    job_id = sys.argv[1]
else:
    job_id = input('Enter target ID of job: ')

assert job_id is not None, 'Job ID expected.'

job_filter = { '_id': job_id }
docu_count = collection.count_documents(filter=job_filter)
assert docu_count == 1, 'There are more than 1 job satify the requirement, but %d are found.' % docu_count

# %% Move existing data to new field
for update_instruction in [{'$rename': {
        'downloaded': 'incomplete_downloaded'
}}, {'$set': {
        'downloaded': False
}}]:
    collection.update_one(filter=job_filter, update=update_instruction)