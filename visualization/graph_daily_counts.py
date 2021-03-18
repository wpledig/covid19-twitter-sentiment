import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

"""
Graphs number of tweets per day + weekly running average
"""


input_file = "../exploration/days_by_counts.csv"


def running_mean(x, N):
    """
    Function that calculates the running mean of data. 
    The inputs are x, the data, and N, the length of the running mean window.
    The output is the running mean of the input data.
    """
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N) 


df = pd.read_csv(input_file, parse_dates=['day'], infer_datetime_format=True)
plt.figure(figsize=(10, 6))
mean = running_mean(df['count'].to_numpy(), 7) # Calculate weekly (N = 7 days) running average.

# Plotting count, day, and weekly mean. 
plt.plot(df['day'], df['count'])
plt.plot(df['day'][3:-3], mean, color='red', label='Weekly Average')

# Formatting plot
plt.legend()
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.title('Number of English Tweets in the US about COVID-19 per Day')

# plt.xticks(rotation='vertical')
# plt.locator_params(axis='x', nbins=12)
plt.savefig('daily_counts.png')
plt.show()
