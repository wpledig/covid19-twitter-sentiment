import tweepy
import json
import sys
import pandas as pd
from time import sleep

"""
Used after get_location_counts. Adds latitude and longitude to pre-existing location data.
This can take a VERY long time to run, so modifies the location_data.csv file in place
This honestly will probably break if location_data doesn't exist, i'll fix that eventually
"""


# Eliminates annoying Pandas warning
pd.set_option('mode.chained_assignment', None)

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


df = pd.read_csv("location_data.csv")
# df["name"] = ""
# df["full_name"] = ""
# df["place_type"] = ""
# df["lng"] = 0.0
# df["lat"] = 0.0

for i in range(df.shape[0]):
    # Stop collecting data-collection for locations under 1 instance
    if df["count"][i] <= 5 or df["lng"][i] != 0.0:
        continue
    location_id = df["location_id"][i]
    geo_data = api.geo_id(location_id)
    df["name"][i] = geo_data.name
    df["full_name"][i] = geo_data.full_name
    df["place_type"][i] = geo_data.place_type
    df["lat"][i] = geo_data.centroid[1]
    df["lng"][i] = geo_data.centroid[0]
    sleep(8)
    if i % 5 == 0:
        df.to_csv("location_data.csv", index=False)
    if i % 100 == 0:
        print("Completed ", i)
        # sleep(10)

df.to_csv("location_data.csv", index=False)
