from dotenv import load_dotenv
import pymongo
from pytrends.request import TrendReq
import requests
# from bson.binary import Binary
from datetime import datetime, timedelta

load_dotenv()

client = pymongo.MongoClient('mongodb://localhost:27017')
collection = client['longcv'].get_collection('jobs')

pytrends = TrendReq(
    hl='en', tz=0,
    retries=3,
    backoff_factor=0.5,
    proxies=[]
)

# while (True):
if True:
    # filter_object = {
    #     "downloaded": False,
    #     "last_attempt": {
    #         "$lt": datetime.now() - timedelta(seconds=15)
    #     }
    # }

    # job = collection.find_one_and_update(
    #     filter=filter_object,
    #     update={
    #         "$set": {
    #             "last_attempt": datetime.now()
    #         }
    #     },
    #     sort=[
    #         ("last_attempt", pymongo.DESCENDING),
    #     ]
    # )
    # # print(f"{filter_object=}")

    # if job is None:
    #     break

    # id = job.get('_id')
    # kw_list = [job.get('keyword')]
    # timeframe = '%s %s' % (
    #     job.get('start_date').strftime("%Y-%m-%d"),
    #     job.get('end_date').strftime("%Y-%m-%d")
    # )
    # print(f"{id=}")
    # print(f"{kw_list=}")
    # print(f"{timeframe=}")
    # exit(0)

    kw_list = ['/g/11q8h3trz5']
    timeframe = '2020-01-02 2020-01-30'

    # try:
    if True:
        pytrends.build_payload(
            kw_list=kw_list,
            cat=0,
            timeframe=timeframe,
            geo=''
        )

        data = pytrends.interest_over_time()

        print(data)

        # collection.update_one(filter={
        #     "_id": job["_id"]
        # }, update={
        #     "$set": {
        #         "downloaded": data
        #     }
        # })

    #     if True:  # Do some checking
    #         # Send a heartbeat
    #         requests.post(
    #             'https://nixklai.heartbeat.sh/beat/219-VM1?warning=15&error=25')

    # except requests.exceptions.RetryError:
    #     exit(0)
