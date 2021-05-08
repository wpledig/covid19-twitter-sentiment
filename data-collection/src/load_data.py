import sys
from github import Github
import wget
import gzip
import os
import pandas as pd
import tweepy
import json

sys.path.append(os.path.abspath("../lib"))
from github_processing import process_daily_contents


"""
Downloads daily CSV files from the Panacea Lab dataset after filtering for only english + US data
"""

""" Global constant variables """
# Date to start collecting daily data from
START_DATE = '2020-07-26'

# Eliminates annoying Pandas warning
pd.set_option('mode.chained_assignment', None)

# Information about the GitHub repo for the source dataset
with open('../api_keys.json') as f:
    keys = json.load(f)

g = Github(keys['github_access'])
repo = g.get_repo("thepanacealab/covid19_twitter")

# Iterate over each folder of daily data in the dataset repository
contents = repo.get_contents("dailies")
for daily_folder in contents:
    if daily_folder.type == 'dir':
        if daily_folder.name < START_DATE:
            continue
        sub_contents = repo.get_contents(daily_folder.path)
        process_daily_contents(sub_contents, daily_folder.name)

