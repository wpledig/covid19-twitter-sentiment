import tweepy
import json
import sys
import pandas as pd
from time import sleep
import os

sys.path.append(os.path.abspath("../../data-collection/lib"))
from twitter_api import load_twitter_api

"""
Used after get_location_counts. Adds latitude and longitude to pre-existing location data.
This can take a VERY long time to run, so it modifies the location_data.csv file in place
"""

# Eliminates annoying Pandas warning
pd.set_option('mode.chained_assignment', None)


# Connect to the Twitter API
api = load_twitter_api('../../data-collection/api_keys.json')

# Load the list of location data from checkpointed file, if exists
if os.path.exists("../data/location_data.csv"):
    df = pd.read_csv("../data/location_data.csv")
else:
    df = pd.read_csv("../data/locations_by_counts.csv")
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
