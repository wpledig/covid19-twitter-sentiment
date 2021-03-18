import tweepy
import json
import sys
import pandas as pd
from time import sleep
import os

"""
Used after get_location_counts. Adds latitude and longitude to pre-existing location data.
This can take a VERY long time to run, so it modifies the location_data.csv file in place
"""


# Eliminates annoying Pandas warning
pd.set_option('mode.chained_assignment', None)


# Connect to the Twitter API
with open('../data-collection/api_keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, retry_delay=60, retry_count=5,
                 retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit_notify=True)

if api.verify_credentials() == False:
    print("Your Twitter api credentials are invalid")
    sys.exit()
else:
    print("Your Twitter api credentials are valid.")

# Load the list of location data from checkpointed file, if exists
if os.path.exists("location_data.csv"):
    df = pd.read_csv("location_data.csv")
else:
    df = pd.read_csv("locations_by_counts.csv")
    df["lng"] = 0.0
    df["lat"] = 0.0

for i in range(df.shape[0]):
    # Don't collect latitude or longitude if location has less than 5 instances, or if they already exist
    if df["count"][i] <= 5 or df["lng"][i] != 0.0:
        continue
    location_id = df["location_id"][i]
    # Retrieve latitude / longitude of location from Twitter API
    geo_data = api.geo_id(location_id)
    df["lat"][i] = geo_data.centroid[1]
    df["lng"][i] = geo_data.centroid[0]
    # Sleep to avoid API rate-limits
    sleep(8)
    # Save checkpoint of data collection to CSV
    if i % 5 == 0:
        df.to_csv("location_data.csv", index=False)
    if i % 100 == 0:
        print("Completed ", i)

df.to_csv("location_data.csv", index=False)
