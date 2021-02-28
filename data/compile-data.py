import os
import pandas as pd

data_columns = ['tweet_id', 'date', 'time']

compiled_data = pd.DataFrame(columns=data_columns)

for file in os.listdir("us_filtered"):
    df = pd.read_csv("us_filtered/" + file)
    df = df.drop(columns=['lang', 'country_code'])
    compiled_data = pd.concat([compiled_data, df])

compiled_data.to_csv('complete_filtered_en_US.csv', index=False)

