import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

comp_df = pd.read_csv("../sentiment-tagging/data/vader_compound_dailies.csv", parse_dates=['day'], infer_datetime_format=True)
emo_df = pd.read_csv("../sentiment-tagging/data/txt2emotion_dailies.csv", parse_dates=['day'], infer_datetime_format=True)

pos_df = pd.read_csv("../exploration/data/positivty_rate.csv", parse_dates=['date'], infer_datetime_format=True)

case_df = pd.read_csv("../data-collection/data/nytimes-us.csv", parse_dates=['date'], infer_datetime_format=True)
case_df["new_cases"] = 0
for index, row in case_df.iterrows():
    if index > 1:
        case_df["new_cases"][index] = case_df["cases"][index] - case_df["cases"][index - 1]

# Trim set of cases to date range found in Tweet dataset
case_df = case_df[case_df["date"] >= comp_df['day'][0]]
case_df = case_df[case_df["date"] <= comp_df['day'][comp_df.shape[0] - 1]]
case_df = case_df.reset_index(drop=True)

pos_df = pos_df[pos_df["date"] >= comp_df['day'][0]]
pos_df = pos_df[pos_df["date"] <= comp_df['day'][comp_df.shape[0] - 1]]
pos_df = pos_df.reset_index(drop=True)


scaler = MinMaxScaler(feature_range=(0, 1))

# scale day of week to range 0-6 for mon-sun
day_of_week = (comp_df.index.to_numpy() - 1) % 7
# TODO: NOTE: no scaling results in lower validation loss, but scaling makes things smoother
day_scaled = day_of_week.reshape(-1, 1)
# day_scaled = scaler.fit_transform(day_of_week.reshape(-1, 1))
print(day_scaled)

comp_scaled = scaler.fit_transform(comp_df['average_compound'].to_numpy().reshape(-1, 1))
# comp_df['average_compound'] = comp_scaled

emo_df['sad'] = scaler.fit_transform(emo_df['sad'].to_numpy().reshape(-1, 1))
emo_df['angry'] = scaler.fit_transform(emo_df['angry'].to_numpy().reshape(-1, 1))
emo_df['surprise'] = scaler.fit_transform(emo_df['surprise'].to_numpy().reshape(-1, 1))
emo_df['fear'] = scaler.fit_transform(emo_df['fear'].to_numpy().reshape(-1, 1))
emo_df['happy'] = scaler.fit_transform(emo_df['happy'].to_numpy().reshape(-1, 1))

emo_scaled = emo_df.to_numpy()[:, 1:]

new_cases_scaled = scaler.fit_transform(case_df['new_cases'].to_numpy().reshape(-1, 1))
pos_rate_scaled = scaler.fit_transform(pos_df['pos_rate'].to_numpy().reshape(-1, 1))
# case_df['new_cases'] = new_cases_scaled



# shape should be (215, 6)
full_scaled = np.concatenate((comp_scaled, emo_scaled, day_scaled), axis=1)

train_len = round(len(comp_scaled) * 1.0)
test_len = round(len(full_scaled) * 0.15)
valid_len = round(len(full_scaled) * 0.05)

# TODO: try training on end and test on start? (prob better results lol)
# could also try setting up intervals w/ lag and splitting data randomly on that
# TODO: swap train and test??
full_train = full_scaled[0: train_len, :]
full_test = full_scaled[train_len: train_len + test_len, :]

cases_train = new_cases_scaled[0: train_len, :]
cases_test = new_cases_scaled[train_len: train_len + test_len, :]

pos_rate_train = pos_rate_scaled[0: train_len, :]
pos_rate_test = pos_rate_scaled[train_len: train_len + test_len, :]


def set_lag(x_set, y_set, lag):
    x_data = []
    y_data = []
    for i in range(len(x_set) - lag - 1):
        x_data.append(x_set[i: (i + lag), :])
        y_data.append(y_set[i + lag, 0])
    return np.array(x_data), np.array(y_data)


lag_size = 50
x_train, y_train = set_lag(full_train, pos_rate_train, lag_size)
x_test, y_test = set_lag(full_test, pos_rate_test, lag_size)

print(x_train)

# x_train = np.reshape(x_train, (len(x_train), 6, lag_size))
# x_test = np.reshape(x_test, (len(x_test), 6, lag_size))
#
# print(x_train)

x_train = np.asarray(x_train).astype('float32')

"""
lag = 14
model.add(LSTM(10, input_shape=(1, lag_size)))
model.add(Dense(1))
w/ 500 epochs, 5 batch size:
loss: 0.0039 - val_loss: 0.0750

dp: 0.5 -> loss: 0.0209 - val_loss: 0.0294
"""

num_features = 7

model = Sequential()

model.add(LSTM(10, return_sequences=True, input_shape=(lag_size, num_features)))
model.add(Dropout(0.5))
#
# model.add(LSTM(10, return_sequences=True))
# model.add(Dropout(0.5))
#
# model.add(LSTM(10, return_sequences=True))
# model.add(Dropout(0.1))
#
# model.add(LSTM(10))
# model.add(Dropout(0.1))

model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit(x_train, y_train, validation_split=0.2, epochs=500, batch_size=20, verbose=2)

plt.figure(figsize=(10, 4))
plt.plot(history.history['loss'], label='Training')
plt.plot(history.history['val_loss'], label='Validation')
plt.legend()
plt.xlabel('Epoch', fontsize=14)
plt.ylabel('Mean Squared Error', fontsize=14)
plt.title('Testing Results of LSTM Model with Window Size = ' + str(lag_size), fontsize=17)

plt.show()

y_hat = model.predict(x_train)

print(y_hat.shape)

y_hat = np.mean(y_hat, axis=1)
#
# print(y_hat.shape)
# y_hat = np.concatenate((y_hat, x_train[:, -5:]), axis=1)
y_hat = scaler.inverse_transform(y_hat)
# y_hat = y_hat[:, 0]

# y_hat = y_hat.reshape(len(y_hat), 1)
# y_hat = scaler.inverse_transform(y_hat)


y_train = scaler.inverse_transform(y_train.reshape(len(y_train), 1))

print(y_hat.shape)
print(y_train.shape)


print('data size: ', len(x_train))

fig, ax = plt.subplots(figsize=(8, 4))

valid_ind = round(len(x_train) * 0.8)
print(valid_ind)
print(y_hat[:valid_ind, :].shape)
print(y_hat[valid_ind:, :].shape)

trimmed_dates = comp_df['day'][lag_size + 1:]

ax.plot(trimmed_dates[:valid_ind], y_hat[:valid_ind, :], label='Training')
ax.plot(trimmed_dates[valid_ind:], y_hat[valid_ind:, :], label='Validation')
ax.plot(trimmed_dates, y_train, label='Real Data')
ax.legend()
# ax.axis('off')

plt.show()
fig.savefig('demo.png', transparent=True)

