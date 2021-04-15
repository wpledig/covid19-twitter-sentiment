from collections import defaultdict
import pandas as pd
import datetime


def get_daily_avg(input_file, output_file, aggr_funcs, aggr_names):
    """
    Aggregates the daily average of some value from an inputted CSV of timestamped values and saves to a new CSV file
    :param input_file: path to input CSV file of timestamped values (timestamp assumed to be in "created_at" field)
    :param output_file: file to save resulting daily averages to
    :param aggr_funcs: list of functions where, given a line from input_file, return a value to be averaged by day
    :param aggr_names: list of names of values for the functions in aggr_funcs
    """
    daily_aggrs = []
    for aggr in aggr_funcs:
        daily_aggrs.append(defaultdict(float))
    daily_counts = defaultdict(int)

    num_counted = 0
    df = pd.read_csv(input_file)
    print("Filesize: ", df.shape)
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

    # Save counts to CSV
    df2 = pd.DataFrame(daily_avgs).transpose().reset_index()
    aggr_names.insert(0, 'day')
    df2.columns = aggr_names
    df2.to_csv(output_file, index=False)