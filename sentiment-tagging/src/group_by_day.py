import sys
import os

sys.path.append(os.path.abspath("../lib"))
from aggregation import get_daily_avg

# Get daily average of VADER sentiment
get_daily_avg("../data/stemmed_vader_tagged.csv", "../data/vader_compound_dailies.csv", [lambda x: x.comp], ['comp'])

# Get daily average of Text2Emotion values
get_daily_avg("../data/txt2emotion_stemmed_tagged.csv", "../data/txt2emotion_dailies.csv",
              [lambda x: x.sad, lambda x: x.angry, lambda x: x.surprise, lambda x: x.fear, lambda x: x.happy],
              ['sad', 'angry', 'surprise', 'fear', 'happy'])


