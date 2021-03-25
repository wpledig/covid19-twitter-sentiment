import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

df = None


def running_mean(x, N):
    """
    Computes the running average over a sliding window
    :param x: a Numpy array of input data
    :param N: the sliding window size
    :return: the running average of x over a sliding window of size N
    """
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def plot_data(input_file, label):
    df = pd.read_csv(input_file, parse_dates=['day'], infer_datetime_format=True)

    # Calculate weekly (N = 7 days) running average.
    w_mean = running_mean(df['average_pos_diff'].to_numpy(), 7)
    m_mean = running_mean(df['average_pos_diff'].to_numpy(), 30)

    # Plotting count, day, and weekly mean.
    # plt.plot(df['day'], df['average_pos_diff'], label=label)
    # plt.plot(df['day'][3:-3], w_mean, label=label + ' Weekly Average')
    plt.plot(df['day'][14:-15], m_mean, label=label + ' Monthly Average')


plot_data("original_daily_pos_diff.csv", "Original")
plot_data("cleaned_daily_pos_diff.csv", "Cleaned")
plot_data("stemmed_daily_pos_diff.csv", "Stemmed")

plt.axhline(y=0.0)
# Formatting plot
plt.legend()
plt.show()

