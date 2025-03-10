# %%
import os
import sys
sys.path.append(os.getcwd())

# %%
import asyncio
import time
import random
from datetime import datetime, timedelta

# %%
import pymongo
from bson.binary import Binary
from playwright.async_api import async_playwright

# %%
from playwright_scrapper import scrap_gt_page
from notifier import Notifier

# %%
machine_name = os.getenv('MACHINE_NAME')
print('[i]', f"{machine_name=}")

# %%
# =============================================================================
# client = pymongo.MongoClient('mongodb://localhost:27017')
# collection = client['longcv'].get_collection('jobs')
# =============================================================================

# %%
notifier = Notifier()

uncomplete_job_filter = {
    "downloaded": False,
    "last_attempt": {
        "$gte": datetime.fromisoformat("1970-01-01 00:00:00"),
        "$lt": datetime.now() - timedelta(seconds=120)
    }
}


async def main():
    async with async_playwright() as playwright:
        backoff_sleep_seconds = 3

        while(True):      
            job = collection.find_one_and_update(filter=uncomplete_job_filter, update={
                "$set": {
                    "last_attempt": datetime.now()
                }
            }, sort=[
                ("last_attempt", pymongo.ASCENDING),
                ('start_date', pymongo.DESCENDING),
            ])
            
            if job is None:
                print(' [i]', 'No new job is found. Will wait...')
                time.sleep(20)
                continue

            _id         = job['_id']
            range_start = job['start_date'].date()
            range_end   = job['end_date'].date()
            tag         = job['keyword']
            region      = job.get('region') or ""

            print(f" [v] New job found. ID={_id}")

            range_start_string = range_start.strftime("%Y-%m-%d")
            range_end_string   = range_end.strftime("%Y-%m-%d")

            notifier.inform_start(data=job.get('_id').encode('utf-8'))
            
            random_second = random.randint(2_000, 5_000) / 1000
            print(f" [v] Task obtained. Will fire request in {random_second} seconds...")
            time.sleep(random_second)

            try:
                print(f" [?] Downloading {tag} during from {range_start_string} to {range_end_string}...")
                ### Use Playwright
                df = await scrap_gt_page(
                    playwright,
                    KEYWORD=tag,
                    START_DATE=range_start_string,
                    END_DATE=range_end_string
                )
                print(" [v] Downloaded:", f"from {range_start_string} to {range_end_string}", df.shape)


                if 'isPartial' in df.columns:
                    df.drop(columns=['isPartial'], inplace=True)


                df.to_pickle(f'./temp-{machine_name}.pkl')
                encoded = None
                with open(f'./temp-{machine_name}.pkl', 'rb') as f:
                    encoded = Binary(f.read())


                collection.update_one(
                    filter={"_id": _id}, 
                    update={
                        "$set": {
                            "downloaded": encoded,
                            "df_length": len(df),
                        }
                    }
                )
                print(" [v] Saved to Mongo.")

                notifier.inform_exit_status(
                    (range_end - range_start).days
                    + 1 
                    - len(df)
                )
                print(f" [v] Ping sent.")
                    
                random_second = random.randint(2_000, 8_000) / 1000
                print(f" [i] Going back in {random_second} seconds...")
                time.sleep(random_second)
            
            except Exception as e:
                print(e)

                backoff_sleep_seconds = backoff_sleep_seconds / 2 + random.randint(0, 10 * 1000) / 1000 * (random.randint(1, 2) - 1)
                backoff_sleep_seconds = abs(backoff_sleep_seconds)
                
                print(f" [w] Hit by 429. Will sleep for {backoff_sleep_seconds} seconds...")
                time.sleep(backoff_sleep_seconds)
                continue
asyncio.run(main())