import math
import sys
from github import Github
import wget
import gzip
import os
import pandas as pd
import tweepy
import json
from time import sleep

"""
Downloads daily CSVs after filtering for only english + US data
"""

TWEET_BATCH_SIZE = 100

# Eliminates annoying Pandas warning
pd.set_option('mode.chained_assignment', None)

g = Github("247e667a9c8eaa6104e840c357e4353ce35065ae")
repo = g.get_repo("thepanacealab/covid19_twitter")

with open('api_keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, retry_delay=60 * 3, retry_count=5,
                 retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit_notify=True)

if api.verify_credentials() == False:
    print("Your Twitter api credentials are invalid")
    sys.exit()
else:
    print("Your Twitter api credentials are valid.")


def extract_country_code(tweet):
    if not hasattr(tweet, 'place') or tweet.place is None:
        return None
    return tweet.place.country_code


# Takes a list of tweet ids and returns a list of their country codes (if available)
def get_tweet_country_code(batch):
    back_off_counter = 1
    tweets = []
    while True:
        try:
            tweets = api.statuses_lookup(batch, include_entities=False, trim_user=True, map_=True)
            break
        except tweepy.TweepError as ex:
            print('Caught the TweepError exception:\n %s' % ex)
            sleep(30 * back_off_counter)  # sleep a bit to see if connection Error is resolved before retrying
            back_off_counter += 1  # increase backoff
            continue
    return list(map(extract_country_code, tweets))


def process_file(file, datestring):
    df = pd.read_csv(file, sep="\t")
    # Add country code column if none exists
    if 'country_code' not in df.columns:
        return
        # TODO: add language
        df['country_code'] = None
        file_length = len(df)
        i = int(math.ceil(float(file_length) / 100))
        start = 0
        end = TWEET_BATCH_SIZE
        for segment in range(i):
            print('currently getting {} - {} / {}'.format(start, end, file_length))
            sleep(6)  # Needed to prevent hitting API rate limit
            id_batch = df['tweet_id'][start:end].tolist()
            # Get tweet country code
            country_codes = get_tweet_country_code(id_batch)
            # TODO: this is giving a warning - look into that
            df['country_code'][start:end] = country_codes
            # print(df[df['country_code'] == 'US'])

            # Increment sliding window
            start += TWEET_BATCH_SIZE
            end += TWEET_BATCH_SIZE

    # Filter data-collection by US only
    print("Saving data-collection for " + datestring)
    filtered_df = df[df['country_code'] == 'US']
    filtered_df = filtered_df[filtered_df['lang'] == 'en']
    filtered_df.to_csv("data/us_filtered/{}_US_clean.csv".format(datestring), index=False)


contents = repo.get_contents("dailies")
for daily_folder in contents:
    if daily_folder.type == 'dir':
        if daily_folder.name < '2020-07-26':
            continue
        print(daily_folder.name)
        sub_contents = repo.get_contents(daily_folder.path)
        for content_file in sub_contents:
            if content_file.name.endswith('clean-dataset.tsv.gz') \
                    and content_file.name != '2020-07-21.json.gz_clean-dataset.tsv.gz':
                wget.download(content_file.download_url, out='temp.tsv.gz')
                with gzip.open('temp.tsv.gz', 'rb') as f_in:
                    process_file(f_in, daily_folder.name)
                # Deletes the compressed GZ file
                os.remove("temp.tsv.gz")
