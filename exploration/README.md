# `exploration`

## Description

These files contain code that aggregates different features of the dataset, such as the number of tweets per day or location.

## Usage
The code in this section should be run in the following order.
1. `get_location_counts.py` 

    This file calculates the number of tweets for each location (using a tweet's `location_id` field) and stores that 
    information in a CSV file titled `locations_by_counts.csv`.

2. `add_location_data.py` 

    This file calls the Twitter API to retrieve the latitude and longitude for the locations in the file produced by the
    previous block of code. This can take a long time to run, so progress will be saved intermittently to `location_data.csv`.

3. `get_daily_counts.py` 

    This file calculates the number of tweets per day and stores that information in a CSV file titled `days_by_counts.csv`.
