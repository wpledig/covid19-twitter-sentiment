# `data-collection`

## Description
This directory contains all of the code to pull the Panacea Lab dataset from the internet, as well as to perform all
required data wrangling. 

To avoid the long runtime that this process has, please download the files stored at the link below and put them
in the `data` folder in your local version of the repository.

The files for the dataset can be found at https://rice.box.com/s/d7r2z48tkrw3q894nr848kwwom1jtsd9

## Usage

The following steps must be performed, in order, to compile the full dataset we will be using for this project.

1. Create a file in this directory titled `api_keys.json` that contains your Twitter API credentials.
    
    This should be a simple JSON object with the following fields: `consumer_key`, `consumer_secret`, `access_token`, 
    and `access_token_secret`.
    
2. Run the Python file `load_data.py`

    This file will download CSV files full of Tweet IDs for each day from `START_DATE` (defined at the top of the file)
    to the current day and save them to the folder `./data/us_filtered/`. These files will also be filtered to remove
    tweets that are either written in a language other than English or originate from a country other than the United States.
    
    Note that files in the source data set from before July 26th, 2020 are not tagged with language or country code, so
    attempting to download these files will lead to much longer runtime as the Twitter API must be called to obtain
    these fields prior to filtering.
    
3. Run the Python file `compile_data.py`

    This file will combine the CSV files downloaded in the previous step into a single CSV file, 
    `./data/complete_filtered_en_US.csv`.
    
4. Run the Python file `get_metadata.py`

    This file was obtained from Panacea Lab's toolkit for processing social media data. It takes a variety of 
    command-line arguments (which you can find more about by running it with the `-h` flag), but we recommend running it
    with the following: `python get_metadata.py -k api_keys.json -i data/complete_filtered_en_US.csv -o data/complete_en_US`
    
    Note that this file makes many calls to the Twitter API (which has strict rate-limit rules), so it can take around
    a very long time to finish running.
    
5. Run the Python file `load_ngrams.py`

    This file aggregates n-gram counts per day from the original dataset and stores them in the `data` directory. 