import sys
import os
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sys.path.append(os.path.abspath("../lib"))
from analysis_helper import perform_analysis_tagging


nltk.download('vader_lexicon')

perform_analysis_tagging("../../data-collection/data/complete_en_US.csv",
                         "../data/stemmed_vader_tagged.csv",
                         SentimentIntensityAnalyzer().polarity_scores,
                         ['neg', 'neu', 'pos', 'compound'])

