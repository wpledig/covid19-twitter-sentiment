import sys
import pandas as pd
import os
import text2emotion as te

sys.path.append(os.path.abspath("../lib"))
from clean_tweets import clean_tweet, stem_tweet

pd.set_option('mode.chained_assignment', None)

orig_text = pd.read_csv('../../data-collection/data/complete_en_US.csv', encoding='utf8')
clean_text = pd.read_csv('../../data-collection/data/complete_en_US.csv', encoding='utf8')
stem_text = pd.read_csv('../../data-collection/data/complete_en_US.csv', encoding='utf8')

def init_df(df):
    df['sad'] = 0.0
    df['angry'] = 0.0
    df['surprise'] = 0.0
    df['fear'] = 0.0
    df['happy'] = 0.0

init_df(orig_text)
init_df(clean_text)
init_df(stem_text)

def print_sentiment(df, i, text):
    analysis = te.get_emotion(text)
    df['sad'][i] = analysis['Sad']
    df['angry'][i] = analysis['Angry']
    df['fear'][i] = analysis['Fear']
    df['surprise'][i] = analysis['Surprise']
    df['happy'][i] = analysis['Happy']

for index, row in orig_text.iterrows():
    stripped_text = row.text[2:-1]
    print_sentiment(orig_text, index, stripped_text)

    cleaned_text = clean_tweet(stripped_text)
    print_sentiment(clean_text, index, cleaned_text)

    stemmed_tweet = stem_tweet(cleaned_text)
    print_sentiment(stem_text, index, stemmed_tweet)

    if index % 100 == 0:
        print("Completed #", index)

# print(orig_text)
orig_text.to_csv("original_tagged.csv", index=False)
clean_text.to_csv("cleaned_tagged.csv", index=False)
stem_text.to_csv("stemmed_tagged.csv", index=False)