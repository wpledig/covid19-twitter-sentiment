# PROJECT NAME (TODO)

## Project Description
TODO

## Usage
All of the code in this project uses Python 3.

The code for this project is separated into different folders based on function, and should be run in a designated order. Please see below for their descriptions.

### Folders
1. `data-collection`
    <p>
    All of the code needed to load / clean the dataset, as well as the files containing the data itself.
    </p>
2. `exploration`
    <p>
    Code to aggregate different features of the raw dataset, and the files representing the results of those.
    </p>
3. `visualization`
    <p>
    Code to create visualizations/graphs of the data (and the image files for those visualizations).
    </p>

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
