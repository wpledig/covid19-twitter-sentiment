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


# Download VADER lexicon if not saved locally
nltk.download('vader_lexicon')
stem_df = pd.read_csv("../../data-collection/data/complete_en_US.csv", encoding='utf8')

# Initialize Dataframe fields
init_df(stem_df, ['neg', 'neu', 'pos', 'comp', 'polar', 'subj'])

# Iterate over all tweets in dataset
for index, row in stem_df.iterrows():
    # Clean + stem tweet
    stripped_text = row.text[2:-1]
    cleaned_text = clean_tweet(stripped_text)
    stemmed_tweet = stem_tweet(cleaned_text)

    # Analyze sentiment with VADER and record scores
    score = SentimentIntensityAnalyzer().polarity_scores(stemmed_tweet)
    stem_df['neg'][index] = score['neg']
    stem_df['neu'][index] = score['neu']
    stem_df['pos'][index] = score['pos']
    stem_df['comp'][index] = score['compound']

    if index % 100 == 0:
        print("Completed #", index)

# Save analyzed sentiment to CSV
stem_df.to_csv("../data/stemmed_vader_tagged.csv", index=False)