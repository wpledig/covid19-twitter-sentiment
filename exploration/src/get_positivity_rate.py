import json
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv('../../data-collection/data/covid_testing_results.csv', parse_dates=['date'], infer_datetime_format=True)


agg_df = df.groupby(by=['date', 'overall_outcome']).agg({'new_results_reported': 'sum'}).reset_index()

print(agg_df)

# print(agg_df[agg_df['overall_outcome'] == 'Positive'])

# TODO: rename this df
test_df = pd.DataFrame()

test_df['date'] = agg_df[agg_df['overall_outcome'] == 'Positive'].reset_index()['date']

test_df['pos'] = agg_df[agg_df['overall_outcome'] == 'Positive'].reset_index()['new_results_reported']
test_df['neg'] = agg_df[agg_df['overall_outcome'] == 'Negative'].reset_index()['new_results_reported']
test_df['inc'] = agg_df[agg_df['overall_outcome'] == 'Inconclusive'].reset_index()['new_results_reported']

# test_df = test_df.set_index('date')

test_df['total'] = test_df['pos'] + test_df['neg'] + test_df['inc']

test_df['pos_rate'] = test_df['pos'] / test_df['total']

# plt.figure(figsize=(10, 6))
# plt.plot(test_df['date'], test_df['pos_rate'])
# plt.legend()
# plt.show()
# print(test_df[test_df['date'] > '2021-03-01'])

print(test_df['2020-12-20' < test_df['date']][test_df['date'] < '2020-12-31'])

test_df.to_csv("../data/positivity_rate.csv", index=False)


