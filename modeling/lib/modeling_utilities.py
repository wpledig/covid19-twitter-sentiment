import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os
import sys


def get_sentiment():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "../../sentiment-tagging/data/vader_compound_dailies.csv"),
                       parse_dates=['day'], infer_datetime_format=True)


def get_emotion():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "../../sentiment-tagging/data/txt2emotion_dailies.csv"),
                       parse_dates=['day'], infer_datetime_format=True)


def get_positivity_rate():
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
    comp_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../sentiment-tagging/data/vader_compound_dailies.csv"),
                          parse_dates=['day'], infer_datetime_format=True)
    days = (comp_df.index.to_numpy() - 1) % 7
    return days.reshape(-1, 1)


def scale_dataset(arr):
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
    plt.figure(figsize=(10, 4))
    plt.plot(history[train_label], label='Training')
    plt.plot(history[valid_label], label='Validation')
    plt.legend()
    plt.xlabel('Epoch', fontsize=14)
    plt.ylabel('Mean Squared Error', fontsize=14)
    plt.title(title, fontsize=17)
    plt.show()


def plot_prediction(dates, real_data, prediction, training_ind, title):
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
