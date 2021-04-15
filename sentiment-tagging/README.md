# `sentiment-tagging`

## Description
This directory contains the code used to calculate and tag sentiment and emotion values for each tweet in the
dataset, and also aggregate those values by daily averages.

## Usage
These files should be run in the following order:

1. `src/vader-analyze.py`

    Tags each tweet with VADER sentiment values and stores that information in `data/stemmed_vader_tagged.csv`
    
2. `src/emotion-analyze.py`

    Tags each tweet with Text2Emotion values and stores that information in `data/txt2emotion_stemmed_tagged.csv`
    
3. `group_by_day`

    Computes the daily averages for both of the CSV files generate by the above files, and stores them in 
    `data/vader_compound_dailies.csv` and `data/txt2emotion_dailies`, respectively.