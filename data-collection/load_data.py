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
Downloads daily CSV files from the Panacea Lab dataset after filtering for only english + US data
"""

""" Global constant variables """
# Number of tweets to include in each batch sent to the Twitter API (max is 100)
TWEET_BATCH_SIZE = 100
# Date to start collecting daily data from
START_DATE = '2020-07-26'

# Eliminates annoying Pandas warning
pd.set_option('mode.chained_assignment', None)

# Information about the GitHub repo for the source dataset
g = Github("247e667a9c8eaa6104e840c357e4353ce35065ae")
repo = g.get_repo("thepanacealab/covid19_twitter")


# Connect to the Twitter API
with open('api_keys.json') as f:
    keys = json.load(f)
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, retry_delay=60 * 3, retry_count=5,
                 retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit_notify=True)

if api.verify_credentials() == False:
    print("Your Twitter API credentials are invalid")
    sys.exit()
else:
    print("Your Twitter API credentials are valid.")


def extract_country_code(tweet):
    """
    :param tweet: a tweet object  (from the Twitter API)
    :return: the tweets country code or None if it does not have one
    """
    if not hasattr(tweet, 'place') or tweet.place is None:
        return None
    return tweet.place.country_code


def get_tweet_country_code(batch):
    """
    Takes a list of tweet ids and returns a list of their country codes
    :param batch: a list of Tweet IDs (should have a length <= 100)
    :return: a list of country codes
    """
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
    """
    Filters a TSV of Tweet IDs from the source dataset (by language and country code) and saves it to disk.
    :param file: the raw source of a TSV from the source dataset
    :param datestring: a string representing the date the input file was collected
    """
    df = pd.read_csv(file, sep="\t")
    # Add country code column if none exists
    if 'country_code' not in df.columns:
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
            df['country_code'][start:end] = country_codes

            # Increment sliding window
            start += TWEET_BATCH_SIZE
            end += TWEET_BATCH_SIZE

    # Filter data-collection by US only
    print("Saving data-collection for " + datestring)
    filtered_df = df[df['country_code'] == 'US']
    filtered_df = filtered_df[filtered_df['lang'] == 'en']
    filtered_df.to_csv("data/us_filtered/{}_US_clean.csv".format(datestring), index=False)


# Iterate over each folder of daily data in the dataset repository
contents = repo.get_contents("dailies")
for daily_folder in contents:
    if daily_folder.type == 'dir':
        if daily_folder.name < START_DATE:
            continue
        print(daily_folder.name)
        sub_contents = repo.get_contents(daily_folder.path)
        for content_file in sub_contents:
            # Download the clean version of each daily dataset to a temporary file, and then process it
            # (We ignore "2020-07-21" because the data for that day in the original dataset was collected improperly)
            if content_file.name.endswith('clean-dataset.tsv.gz') \
                    and content_file.name != '2020-07-21.json.gz_clean-dataset.tsv.gz':
                wget.download(content_file.download_url, out='temp.tsv.gz')
                with gzip.open('temp.tsv.gz', 'rb') as f_in:
                    process_file(f_in, daily_folder.name)
                # Deletes the temporary file for this day
                os.remove("temp.tsv.gz")
