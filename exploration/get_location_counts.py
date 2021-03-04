import json
from collections import defaultdict
import pandas as pd

location_counts = {}

dataset = "../data/complete_en_US"

num_counted = 0

with open(dataset) as inputfile:
    lines = inputfile.readlines()
    print("filesize: ", len(lines))
    for line in lines:
        jline = json.loads(line)
        if jline['place'] is None:
            continue
        location_id = jline['place']['id']
        place = jline['place']
        if location_id not in location_counts.keys():
            location_counts[location_id] = {
                'name': place['name'],
                'full_name': place['full_name'],
                'place_type': place['place_type'],
                'count': 0
            }

        location_counts[location_id]['count'] += 1
        print(json.dumps(jline, indent=4))

        num_counted += 1
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)

df = pd.DataFrame.from_dict(location_counts, orient='index').reset_index()
# df.columns = ['location_id', 'count']
print(df)
df = df.sort_values(by='count', ascending=False)
df.to_csv("locations_by_counts.csv", index=False)

