import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(11, 5))
ax2 = ax1.twinx()


def running_mean(x, N):
    """
    Computes the running average over a sliding window
    :param x: a Numpy array of input data
    :param N: the sliding window size
    :return: the running average of x over a sliding window of size N
    """
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def plot_data(df, field, label):
    # Calculate weekly (N = 7 days) running average.
    w_mean = running_mean(df[field].to_numpy(), 7)
    m_mean = running_mean(df[field].to_numpy(), 30)

    # Plotting count, day, and weekly mean.
    # plt.plot(df['day'], df[field], label=label)
    ax1.plot(df['day'][3:-3], w_mean, label=label + " Weekly Average")
    ax1.plot(df['day'][14:-15], m_mean, color='g', label=label + ' Monthly Average')


# orig_df = pd.read_csv("original_daily_compound.csv", parse_dates=['day'], infer_datetime_format=True)
# clean_df = pd.read_csv("cleaned_daily_compound.csv", parse_dates=['day'], infer_datetime_format=True)
stem_df = pd.read_csv("../data/stemmed_daily_compound.csv", parse_dates=['day'], infer_datetime_format=True)
# stem_df['sad'] -= stem_df['sad'].mean()
# stem_df['angry'] -= stem_df['angry'].mean()
# stem_df['surprise'] -= stem_df['surprise'].mean()
# stem_df['fear'] -= stem_df['fear'].mean()
# stem_df['happy'] -= stem_df['happy'].mean()

# plot_data(orig_df, "Original")
# plot_data(clean_df, "Cleaned")
# plot_data(stem_df, 'polar', "Polarity")
plot_data(stem_df, 'average_compound', "Sentiment")
# plot_data(stem_df, 'angry', "Angry")
# plot_data(stem_df, 'surprise', "Surprise")
# plot_data(stem_df, 'fear', "Fear")
# plot_data(stem_df, 'happy', "Happy")


case_df = pd.read_csv("../../data-collection/data/nytimes-us.csv", parse_dates=['date'], infer_datetime_format=True)
case_df["new_cases"] = 0
for index, row in case_df.iterrows():
    if index > 1:
        case_df["new_cases"][index] = case_df["cases"][index] - case_df["cases"][index - 1]

case_df = case_df[case_df["date"] >= stem_df['day'][0]]
case_df = case_df[case_df["date"] <= stem_df['day'][stem_df.shape[0] - 1]]

# case_df['new_cases_norm'] = case_df['new_cases'] * (stem_df['average_compound'].mean() / case_df['new_cases'].mean())

# case_df['new_cases_norm'] = case_df['new_cases_norm'] - 0.01

case_mean = running_mean(case_df['new_cases'].to_numpy(), 7)

ax2.plot(case_df['date'][14:-15], case_mean[11:-12], color='red', label='New Cases Weekly Average')

ax2.set_ylim(0, 290000)

ax1.axhline(y=0.0, color='black')
# plt.axvline(x=datetime.datetime(2020, 11, 3), linestyle='dashed', color='black')
# Formatting plot
ax1.legend()
ax2.legend(loc='upper right')

plt.title('Sentiment of Tweets about COVID-19 compared to Infection Rate over Time in the US', fontsize=17)
ax1.set_xlabel('Date', fontsize=14)
ax1.set_ylabel('Average Sentiment', fontsize=14)
ax2.set_ylabel('New Cases of COVID-19', fontsize=14)
plt.show()

