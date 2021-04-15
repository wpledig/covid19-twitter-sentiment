import matplotlib.pyplot as plt
import numpy as np


def running_mean(x, N):
    """
    Computes the running average over a sliding window
    :param x: a Numpy array of input data
    :param N: the sliding window size
    :return: the running average of x over a sliding window of size N
    """
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def make_ngram_bar(df, key, end):
    """
    Creates a horizontal bar plot formatted for an input set of n-grams counts.

    :param df: a Dataframe containing columns 'counts' and key
    :param key: the column of df containing the n-grams as a string
    :param end: the number of n-grams
    :return: Nothing.
    """
    # Selecting data to be plotted
    df = df[:end]
    plt.figure(figsize=(10, 7))
    plt.barh(range(df.shape[0]), df['counts'])
    plt.ticklabel_format(style='plain')

    plt.yticks(range(df.shape[0]), df[key])
    plt.gca().invert_yaxis()

    # Creating labels/titles.
    plt.xlabel('Number of Appearances')
    plt.title('25 Most Common Terms in Covid-Related Tweets')
    plt.show()


def plot_avgs(df, plot, field, label, include_daily, include_weekly, include_monthly):
    """
    Graphs a range of time-stamped data on a provided graph
    :param df: source dataframe for the data
    :param plot: plot object for the graph to be plotted on
    :param field: field within df to be plotted
    :param label: label to be used for this data value on the graph
    :param include_daily: if true, include a plot of daily values for the data field
    :param include_weekly: if true, include a plot of weekly averages for the data field
    :param include_monthly: if true, include a plot of monthly averages for the data field
    """
    if include_daily:
        plot.plot(df['day'], df[field], label=label)

    if include_weekly:
        w_mean = running_mean(df[field].to_numpy(), 7)
        plot.plot(df['day'][3:-3], w_mean, label=label + " Weekly Average")

    if include_monthly:
        m_mean = running_mean(df[field].to_numpy(), 30)
        plot.plot(df['day'][14:-15], m_mean, color='g', label=label + ' Monthly Average')