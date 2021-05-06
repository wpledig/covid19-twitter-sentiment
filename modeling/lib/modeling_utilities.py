import numpy as np


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