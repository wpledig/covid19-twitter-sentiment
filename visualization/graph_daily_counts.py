import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

"""
Graphs number of tweets per day + weekly running average
"""


input_file = "../exploration/days_by_counts.csv"


def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


df = pd.read_csv(input_file, parse_dates=['day'], infer_datetime_format=True)
plt.figure(figsize=(10, 6))
mean = running_mean(df['count'].to_numpy(), 7)

plt.plot(df['day'], df['count'])
plt.plot(df['day'][3:-3], mean, color='red', label='Weekly Average')

plt.legend()
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.title('Number of English Tweets in the US about COVID-19 per Day')

# plt.xticks(rotation='vertical')
# plt.locator_params(axis='x', nbins=12)
plt.savefig('daily_counts.png')
plt.show()
