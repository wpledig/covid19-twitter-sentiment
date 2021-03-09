import os
import pandas as pd

"""
Takes a directory of daily CSV files and combines them into a single CSV
"""

data_columns = ['tweet_id', 'date', 'time']

filtered_dir = "data/us_filtered"

compiled_data = pd.DataFrame(columns=data_columns)

for file in os.listdir(filtered_dir):
    df = pd.read_csv(filtered_dir + file)
    df = df.drop(columns=['lang', 'country_code'])
    compiled_data = pd.concat([compiled_data, df])

compiled_data.to_csv('data/complete_filtered_en_US.csv', index=False)

