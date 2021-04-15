import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath("../lib"))
from plot_utilities import running_mean

"""
Graphs number of tweets per day + weekly running average
"""

input_file = "../../exploration/data/days_by_counts.csv"

df = pd.read_csv(input_file, parse_dates=['day'], infer_datetime_format=True)
plt.figure(figsize=(10, 6))
# Calculate weekly (N = 7 days) running average.
mean = running_mean(df['count'].to_numpy(), 7)

# Plotting count, day, and weekly mean. 
plt.plot(df['day'], df['count'])
plt.plot(df['day'][3:-3], mean, color='red', label='Weekly Average')

# Formatting plot
plt.legend()
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.title('Number of English Tweets in the US about COVID-19 per Day')

plt.savefig('../plots/daily_counts.png')
plt.show()
