# DSCI 400 Project

Download link to the dataset can be found at https://rice.box.com/s/d7r2z48tkrw3q894nr848kwwom1jtsd9

Project Description:

Through our project, we will investigate how sentiments expressed about the pandemic on social media interact with public health outcomes, and whether they are an effective predictor of future outcomes.

Our objectives in the project will include:

Sentiment analysis of a large dataset of Twitter posts, ranging across time and space

Analysis of how sentiments interact with public health outcomes over time and space, identifying which sentiments correlate with positive outcomes and which sentiments correlate with negative outcomes

A model which, given sentiment over a time and space, predicts COVID-19 infection and mortality rates

# Exploration

- add_location_data.py retrieves the latitude and longitude of imported data.
- get_daily_counts.py calculates the number of tweets in our data per day and stores that information in a csv file.
- get_location_counts.py calculates the number of tweets in a location (using location_id) and stores that information in a csv file.
