import json
from collections import defaultdict
import pandas as pd

"""
Computes the number of tweets by location_id, and stores that in a CSV
"""

dataset = "../data-collection/data/complete_en_US"

location_counts = {}
num_counted = 0

with open(dataset) as inputfile:
    lines = inputfile.readlines()
    print("filesize: ", len(lines))
    # Iterate over all tweets in the dataset
    for line in lines:
        jline = json.loads(line)
        # Skip tweet if no location is listed
        if jline['place'] is None:
            continue
        location_id = jline['place']['id']
        place = jline['place']
        # If location has not been encountered yet, create new entry in dictionary
        if location_id not in location_counts.keys():
            location_counts[location_id] = {
                'name': place['name'],
                'full_name': place['full_name'],
                'place_type': place['place_type'],
                'count': 0
            }

        # Increment count for current location
        location_counts[location_id]['count'] += 1

        # Print progress to console
        num_counted += 1
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)

# Save counts to CSV file
df = pd.DataFrame.from_dict(location_counts, orient='index').reset_index()
print(df)
df = df.sort_values(by='count', ascending=False)
df.to_csv("locations_by_counts.csv", index=False)

