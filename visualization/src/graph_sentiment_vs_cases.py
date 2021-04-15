import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath("../lib"))
from plot_utilities import running_mean, plot_avgs


fig, ax1 = plt.subplots(figsize=(11, 5))
ax2 = ax1.twinx()

# Plot weekly and monthly average sentiment
stem_df = pd.read_csv("../../sentiment-tagging/data/vader_compound_dailies.csv", parse_dates=['day'], infer_datetime_format=True)
plot_avgs(stem_df, ax1, 'average_compound', "Sentiment", False, True, True)

# Compute daily number of new cases from NY Times data
case_df = pd.read_csv("../../data-collection/data/nytimes-us.csv", parse_dates=['date'], infer_datetime_format=True)
case_df["new_cases"] = 0
for index, row in case_df.iterrows():
    if index > 1:
        case_df["new_cases"][index] = case_df["cases"][index] - case_df["cases"][index - 1]

# Trim set of cases to date range found in Tweet dataset
case_df = case_df[case_df["date"] >= stem_df['day'][0]]
case_df = case_df[case_df["date"] <= stem_df['day'][stem_df.shape[0] - 1]]

# Get weekly running average for cases
case_mean = running_mean(case_df['new_cases'].to_numpy(), 7)

# Plot new cases
ax2.plot(case_df['date'][14:-15], case_mean[11:-12], color='red', label='New Cases Weekly Average')
ax2.set_ylim(0, 290000)

# Legend + label adjustments
ax1.axhline(y=0.0, color='black')
ax1.legend()
ax2.legend(loc='upper right')
plt.title('Sentiment of Tweets about COVID-19 compared to Infection Rate over Time in the US', fontsize=17)
ax1.set_xlabel('Date', fontsize=14)
ax1.set_ylabel('Average Sentiment', fontsize=14)
ax2.set_ylabel('New Cases of COVID-19', fontsize=14)
plt.show()

