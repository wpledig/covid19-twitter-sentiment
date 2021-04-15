# `visualization`

## Description
This directory contains the code needed to generate exploratory visualizations of the dataset, as well as the visualization
images themselves.

## Usage
These files can be ran in any order.
- `src/graph_daily_counts.py` 

    Graphs the number of tweets per day as well as a weekly running average.

- `src/graph_ngrams.py` 

    Plots bar graphs of the counts of the top 25 n-grams in the dataset.

- `src/make-wordcloud.py` 

    Generates a word cloud with the most frequently used words in the collected tweets.

- `src/plot_city_data.py` 

    Plots the number of tweets per city on a map of the United States.

- `src/plot_state_data.py` 

    Creates a heat map of the number of tweets per US state.
    
- `src/graph_sentiment_vs_cases.py` 

    Plots a graph of VADER sentiment overlayed with COVID-19 infection rate.
    
- `src/graph_daily_emotions.py` 

    Creates a graph of weekly averages of emotions relative to their overall average values.

## Examples 

![daily](plots/daily_counts.png?raw=true)

![trigrams](plots/trigrams.png?raw=true)

![terms](plots/terms.png?raw=true)

![city](plots/city_counts.png?raw=true)

![state](plots/state_counts.png?raw=true)