from collections import defaultdict
import pandas as pd
import datetime


def get_daily_avg(input_file, output_file, aggr_funcs, aggr_names):
    daily_aggrs = []
    for aggr in aggr_funcs:
        daily_aggrs.append(defaultdict(float))
    daily_counts = defaultdict(int)

    num_counted = 0
    df = pd.read_csv(input_file)
    print("filesize: ", df.shape)
    for index, row in df.iterrows():

        # Get the current date from the tweet's timestamp
        cur_date = datetime.datetime.strptime(row.created_at, '%a %b %d %H:%M:%S %z %Y')

        # Increment the count of tweets for this date
        daily_counts[cur_date.date()] += 1
        for i in range(len(aggr_funcs)):
            daily_aggrs[i][cur_date.date()] += aggr_funcs[i](row)

        # Print progress update to console
        num_counted += 1
        if num_counted % 1000 == 0:
            print("Counted ", num_counted)

    daily_avgs = [{} for i in range(len(aggr_funcs))]
    for day in daily_counts.keys():
        for i in range(len(aggr_funcs)):
            daily_avgs[i][day] = daily_aggrs[i][day] / daily_counts[day]

    print(daily_avgs)

    # Save counts to CSV
    df2 = pd.DataFrame(daily_avgs).transpose().reset_index()
    print(df2)
    aggr_names.insert(0, 'day')
    df2.columns = aggr_names
    print(df2)
    df2.to_csv(output_file, index=False)


get_daily_avg("../textblob_stemmed_tagged.csv", "textblob_dailies.csv",
              [lambda x: x.polar, lambda x: x.subj],
              ['polar', 'subj'])


