import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os


def get_sentiment():
    """
    Returns a dataframe of the daily average compound sentiment from the Twitter dataset
    """
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "../../sentiment-tagging/data/vader_compound_dailies.csv"),
                       parse_dates=['day'], infer_datetime_format=True)


def get_emotion():
    """
    Returns a dataframe of the daily average emotion vector values from the Twitter dataset
    """
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "../../sentiment-tagging/data/txt2emotion_dailies.csv"),
                       parse_dates=['day'], infer_datetime_format=True)


def get_positivity_rate():
    """
    Returns a dataframe of the daily positivity rate of COVID-19 tests in the US, trimmed to the dates available in the
    Twitter dataset
    """
    comp_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../sentiment-tagging/data/vader_compound_dailies.csv"),
                          parse_dates=['day'], infer_datetime_format=True)
    pos_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../exploration/data/positivity_rate.csv"),
                         parse_dates=['date'], infer_datetime_format=True)

    # Trim positivity rate data to Tweet date range
    pos_df = pos_df[pos_df["date"] >= comp_df['day'][0]]
    pos_df = pos_df[pos_df["date"] <= comp_df['day'][comp_df.shape[0] - 1]]
    pos_df = pos_df.reset_index(drop=True)
    return pos_df


def get_day_of_week():
    """
    Returns a numpy array of the day of the week for each day in the Twitter dataset, where 0 is Monday and 6 is Sunday
    """
    comp_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../sentiment-tagging/data/vader_compound_dailies.csv"),
                          parse_dates=['day'], infer_datetime_format=True)
    days = (comp_df.index.to_numpy() - 1) % 7
    return days.reshape(-1, 1)


def scale_dataset(arr):
    """
    Scales the inputted array to the range [0, 1] based on the array's minimum and maximum
    :param arr: The array to be scaled
    :return: A tuple of the scaled array and the scaler that has been fitted to the array (useful for re-scaling data
    back to the original data range)
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    if len(arr.shape) == 1:
        arr = arr.reshape(-1, 1)
    arr_scaled = scaler.fit_transform(arr)
    return arr_scaled, scaler


def set_lag(x_set, y_set, lag):
    """
    Reshapes an existing dataset to a sliding window of x values
    :param x_set: array of x values (independent variable)
    :param y_set: array of y values (dependent variable)
    :param lag: window size
    :return: reshaped x array, reshaped y array
    """
    x_data = []
    y_data = []
    for i in range(len(x_set) - lag - 1):
        x_data.append(x_set[i: (i + lag), :])
        y_data.append(y_set[i + lag, 0])
    return np.array(x_data), np.array(y_data)


def plot_loss(history, train_label, valid_label, title):
    """
    Plots a graph of training and validation loss over time for a given model
    :param history: an object containing sequences of loss values for training and validation
    :param train_label: the label for training loss values in the "history" object
    :param valid_label: the label for testing loss values in the "history" object
    :param title: string to be used as the title for the outputted graph
    """
    plt.figure(figsize=(10, 4))
    plt.plot(history[train_label], label='Training')
    plt.plot(history[valid_label], label='Validation')
    plt.legend()
    plt.xlabel('Epoch', fontsize=14)
    plt.ylabel('Mean Squared Error', fontsize=14)
    plt.title(title, fontsize=17)
    plt.show()


def plot_prediction(dates, real_data, prediction, training_ind, title):
    """
    Plots a graph of predictions of COVID-19 test positivity rate for a model
    :param dates: range of dates for the predictions/real data (sequence of x values)
    :param real_data: list of data points for actual positivity rate
    :param prediction: list of predicted data points for positivity rate
    :param training_ind: number representing the last index of training data in "prediction" (if set to 0, this function
            assumes no training data is included in "prediction"
    :param title: string for the title of the outputted graph
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    if training_ind > 0:
        ax.plot(dates[:training_ind], prediction[:training_ind], label='Training Prediction')
    ax.plot(dates[training_ind:], prediction[training_ind:], label='Testing Prediction')
    ax.plot(dates, real_data, label='Real Data')
    ax.legend()
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Test Positivity Rate', fontsize=14)
    plt.title(title, fontsize=17)

    plt.show()
