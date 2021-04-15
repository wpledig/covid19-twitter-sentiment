from time import sleep
import math
import wget
import gzip
import os
import pandas as pd
import tweepy
import sys
import json

from twitter_api import load_twitter_api

# Number of tweets to include in each batch sent to the Twitter API (max is 100)
TWEET_BATCH_SIZE = 100

api = load_twitter_api('../api_keys.json')

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
    filtered_df.to_csv("../data/us_filtered/{}_US_clean.csv".format(datestring), index=False)


def process_daily_contents(folder_contents, folder_name):
    """
    Processes a folder of daily data (from the COVID tweet dataset GitHub)
    :param folder: a GitHub folder object
    """
    print(folder_name)
    for content_file in folder_contents:
        # Download the clean version of each daily dataset to a temporary file, and then process it
        # (We ignore "2020-07-21" because the data for that day in the original dataset was collected improperly)
        if content_file.name.endswith('clean-dataset.tsv.gz') \
                and content_file.name != '2020-07-21.json.gz_clean-dataset.tsv.gz':
            wget.download(content_file.download_url, out='temp.tsv.gz')
            with gzip.open('temp.tsv.gz', 'rb') as f_in:
                process_file(f_in, folder_name)
            # Deletes the temporary file for this day
            os.remove("temp.tsv.gz")
