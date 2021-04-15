import json
from collections import defaultdict
import pandas as pd
import datetime

"""
Calculates the number of tweets per day and stores in a CSV
"""

daily_counts = defaultdict(int)

dataset = "../data-collection/data/complete_en_US"

num_counted = 0

# Iterate through every tweet in the dataset
with open(dataset) as inputfile:
    lines = inputfile.readlines()
    print("filesize: ", len(lines))
    for line in lines:
        jline = json.loads(line)
        # Get the current date from the tweet's timestamp
        cur_date = datetime.datetime.strptime(jline["created_at"], '%a %b %d %H:%M:%S %z %Y')

        # Increment the count of tweets for this date
        daily_counts[cur_date.date()] += 1

        # Print progress update to console
        num_counted += 1
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)

# Save counts to CSV
df = pd.DataFrame.from_dict(daily_counts, orient='index').reset_index()
df.columns = ['day', 'count']
print(df)
df.to_csv("days_by_counts.csv", index=False)

