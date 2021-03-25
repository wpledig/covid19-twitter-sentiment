from collections import defaultdict
import pandas as pd
import datetime


def get_daily_avg(input_file, output_file, aggr_func):
    daily_diff_pos_total = defaultdict(float)
    daily_counts = defaultdict(int)

    num_counted = 0
    df = pd.read_csv(input_file)
    print("filesize: ", df.shape)
    for index, row in df.iterrows():

        # Get the current date from the tweet's timestamp
        cur_date = datetime.datetime.strptime(row.created_at, '%a %b %d %H:%M:%S %z %Y')

        # Increment the count of tweets for this date
        daily_counts[cur_date.date()] += 1
        daily_diff_pos_total[cur_date.date()] += row.pos - row.neg

        # Print progress update to console
        num_counted += 1
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)

    daily_avg_pos = {}
    for day in daily_counts.keys():
        daily_avg_pos[day] = daily_diff_pos_total[day] / daily_counts[day]

    print(daily_avg_pos)

    # Save counts to CSV
    df2 = pd.DataFrame.from_dict(daily_avg_pos, orient='index').reset_index()
    df2.columns = ['day', 'average_pos_diff']
    print(df2)
    df2.to_csv(output_file, index=False)


get_pos_diff = lambda x: x.pos - x.neg

get_daily_avg("original_tagged.csv", "original_daily_pos_diff.csv", get_pos_diff)
get_daily_avg("cleaned_tagged.csv", "cleaned_daily_pos_diff.csv", get_pos_diff)
get_daily_avg("stemmed_tagged.csv", "stemmed_daily_pos_diff.csv", get_pos_diff)


