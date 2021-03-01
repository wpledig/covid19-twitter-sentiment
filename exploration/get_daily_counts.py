import json
from collections import defaultdict
import pandas as pd
import datetime

daily_counts = defaultdict(int)

dataset = "../data/complete_en_US"

num_counted = 0

with open(dataset) as inputfile:
    lines = inputfile.readlines()
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

