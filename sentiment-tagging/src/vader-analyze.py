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


positive = 0
negative = 0
neutral = 0
polarity = 0

nltk.download('vader_lexicon')
df = pd.read_csv("../../data-collection/data/complete_en_US.csv", encoding='utf8')


def print_sentiment(text):
    analysis = TextBlob(text)
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    # polarity += analysis.sentiment.polarity
    print(score)
    print(analysis.sentiment)


for index, row in df.iterrows():
    stripped_text = row.text[2:-1]
    print(stripped_text)
    print_sentiment(stripped_text)

    cleaned_text = clean_tweet(stripped_text)
    print(cleaned_text)
    print_sentiment(cleaned_text)

    stemmed_tweet = stem_tweet(cleaned_text)
    print(stemmed_tweet)
    print_sentiment(stemmed_tweet)

    print()
