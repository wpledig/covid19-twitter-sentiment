from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string

from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

sys.path.append(os.path.abspath("../lib"))
from clean_tweets import clean_tweet, stem_tweet


pd.set_option('mode.chained_assignment', None)


def init_df(df):
    df['neg'] = 0.0
    df['neu'] = 0.0
    df['pos'] = 0.0
    df['comp'] = 0.0
    df['polar'] = 0.0
    df['subj'] = 0.0


nltk.download('vader_lexicon')
orig_df = pd.read_csv("../../data-collection/data/complete_en_US.csv", encoding='utf8')
clean_df = pd.read_csv("../../data-collection/data/complete_en_US.csv", encoding='utf8')
stem_df = pd.read_csv("../../data-collection/data/complete_en_US.csv", encoding='utf8')

init_df(orig_df)
init_df(clean_df)
init_df(stem_df)


def print_sentiment(df, i, text):
    analysis = TextBlob(text)
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    df['neg'][i] = score['neg']
    df['neu'][i] = score['neu']
    df['pos'][i] = score['pos']
    df['comp'][i] = score['compound']
    df['polar'][i] = analysis.sentiment.polarity
    df['subj'][i] = analysis.sentiment.subjectivity


for index, row in orig_df.iterrows():
    stripped_text = row.text[2:-1]
    print_sentiment(orig_df, index, stripped_text)

    cleaned_text = clean_tweet(stripped_text)
    print_sentiment(clean_df, index, cleaned_text)

    stemmed_tweet = stem_tweet(cleaned_text)
    print_sentiment(stem_df, index, stemmed_tweet)

    if index % 100 == 0:
        print("Completed #", index)

print(orig_df)
orig_df.to_csv("original_tagged.csv", index=False)
clean_df.to_csv("cleaned_tagged.csv", index=False)
stem_df.to_csv("stemmed_tagged.csv", index=False)