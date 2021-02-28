import json
from collections import defaultdict
import pandas as pd

location_counts = defaultdict(int)

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
        location_counts[location_id] += 1
        # print(json.dumps(, indent=4))

        num_counted += 1
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)

df = pd.DataFrame.from_dict(location_counts, orient='index').reset_index()
df.columns = ['location_id', 'count']
df = df.sort_values(by='count', ascending=False)
df.to_csv("location_id_counts.csv", index=False)

