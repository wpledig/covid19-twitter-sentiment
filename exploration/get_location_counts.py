import json
from collections import defaultdict
import pandas as pd

location_counts = {}

"""
Computes the number of tweets by location_id, and stores that in a CSV
"""

dataset = "../data-collection/data/complete_en_US"

num_counted = 0

# generate dictionary which stores location data from 'dataset'
with open(dataset) as inputfile:
    lines = inputfile.readlines()
    print("filesize: ", len(lines))
    for line in lines: # for each line
        jline = json.loads(line) # interpret each line as a json entry
        if jline['place'] is None: # skip if no place listed
            continue
        location_id = jline['place']['id']
        place = jline['place']
        if location_id not in location_counts.keys(): # if location has not been encountered yet, create new entry
            location_counts[location_id] = { # copy json information into a python dictionary
                'name': place['name'],
                'full_name': place['full_name'],
                'place_type': place['place_type'],
                'count': 0
            }

        location_counts[location_id]['count'] += 1 # add 1 to count within dictionary

        num_counted += 1 # add 1 to total number of locations counted
        if num_counted % 1000 == 0: # every 1000 locations counted, print progress
            print("Counted ", num_counted)

df = pd.DataFrame.from_dict(location_counts, orient='index').reset_index() # generate pandas dataframe from dictionary
# df.columns = ['location_id', 'count']
print(df)
df = df.sort_values(by='count', ascending=False)
df.to_csv("locations_by_counts.csv", index=False) # export dataframe to csv

