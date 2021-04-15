from textblob import TextBlob
import sys
import pandas as pd
import os
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sys.path.append(os.path.abspath("../lib"))
from clean_tweets import clean_tweet, stem_tweet

pd.set_option('mode.chained_assignment', None)


def init_df(df, fields):
    for field in fields:
        df[field] = 0.0


def perform_analysis_tagging(input_file, output_file, analysis_func, fields):
    stem_df = pd.read_csv(input_file, encoding='utf8')

    # Initialize Dataframe fields
    init_df(stem_df, fields)

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
