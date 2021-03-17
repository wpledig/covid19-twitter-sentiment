import json
from collections import defaultdict
import pandas as pd
import datetime

"""
Calculates the number of tweets per day and stores in a CSV
"""

daily_counts = defaultdict(int)     #create a dictionary to store the value of the number of tweets

dataset = "../data-collection/data/complete_en_US"      #define a variable for the dataset 
num_counted = 0         #initialize the number of daily tweets counted to 0

with open(dataset) as inputfile:       
    lines = inputfile.readlines()       #define a variable for each line in the dataset
    print("filesize: ", len(lines))
    for line in lines:             
        jline = json.loads(line)
        # print(json.dumps(jline, indent=4))

        # print(jline["created_at"])
        cur_date = datetime.datetime.strptime(jline["created_at"], '%a %b %d %H:%M:%S %z %Y')
        daily_counts[cur_date.date()] += 1

        num_counted += 1
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)

df = pd.DataFrame.from_dict(daily_counts, orient='index').reset_index()
df.columns = ['day', 'count']
print(df)
df.to_csv("days_by_counts.csv", index=False)

