from textblob import TextBlob
import sys
import pandas as pd
import os
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sys.path.append(os.path.abspath("../lib"))
from clean_tweets import clean_tweet, stem_tweet

pd.set_option('mode.chained_assignment', None)


def perform_analysis_tagging(input_file, output_file, analysis_func, fields):
    """
    Given an inputted CSV of tweets, performs some form of analysis on each tweet and saves the results in a new CSV
    :param input_file: CSV file where each line contains a tweet in the "text" field
    :param output_file: CSV file to save tagged data to
    :param analysis_func: function that takes a string as input and returns an object of values
    :param fields: a list of fields to save from the object returned from analysis_func
    """
    stem_df = pd.read_csv(input_file, encoding='utf8')

    # Initialize Dataframe fields
    for field in fields:
        stem_df[field] = 0.0

    # Iterate over all tweets in dataset
    for index, row in stem_df.iterrows():
        # Clean + stem tweet
        stripped_text = row.text[2:-1]
        cleaned_text = clean_tweet(stripped_text)
        stemmed_tweet = stem_tweet(cleaned_text)

        # Analyze sentiment and record scores
        analysis_res = analysis_func(stemmed_tweet)
        for field in fields:
            stem_df[field][index] = analysis_res[field]

        if index % 100 == 0:
            print("Completed #", index)

    # Save analyzed sentiment to CSV
    stem_df.to_csv(output_file, index=False)
