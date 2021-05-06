import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
import os
import sys

sys.path.append(os.path.abspath("../lib"))
from modeling_utilities import set_lag

# Load datasets
comp_df = pd.read_csv("../../sentiment-tagging/data/vader_compound_dailies.csv", parse_dates=['day'], infer_datetime_format=True)
emo_df = pd.read_csv("../../sentiment-tagging/data/txt2emotion_dailies.csv", parse_dates=['day'], infer_datetime_format=True)
pos_df = pd.read_csv("../../exploration/data/positivty_rate.csv", parse_dates=['date'], infer_datetime_format=True)

# Trim positivity rate data to Tweet date range
pos_df = pos_df[pos_df["date"] >= comp_df['day'][0]]
pos_df = pos_df[pos_df["date"] <= comp_df['day'][comp_df.shape[0] - 1]]
pos_df = pos_df.reset_index(drop=True)

# Create a new feature to represent the day of the week for each data point
day_of_week = (comp_df.index.to_numpy() - 1) % 7
day_scaled = day_of_week.reshape(-1, 1)

# Scale data points to range from 0 to 1
scaler = MinMaxScaler(feature_range=(0, 1))

comp_scaled = scaler.fit_transform(comp_df['average_compound'].to_numpy().reshape(-1, 1))

emo_df['sad'] = scaler.fit_transform(emo_df['sad'].to_numpy().reshape(-1, 1))
emo_df['angry'] = scaler.fit_transform(emo_df['angry'].to_numpy().reshape(-1, 1))
emo_df['surprise'] = scaler.fit_transform(emo_df['surprise'].to_numpy().reshape(-1, 1))
emo_df['fear'] = scaler.fit_transform(emo_df['fear'].to_numpy().reshape(-1, 1))
emo_df['happy'] = scaler.fit_transform(emo_df['happy'].to_numpy().reshape(-1, 1))

emo_scaled = emo_df.to_numpy()[:, 1:]

pos_rate_scaled = scaler.fit_transform(pos_df['pos_rate'].to_numpy().reshape(-1, 1))

# Concatenate all feature sets to one numpy array
full_scaled = np.concatenate((comp_scaled, emo_scaled, day_scaled), axis=1)

train_len = len(comp_scaled)
full_train = full_scaled[0: train_len, :]
pos_rate_train = pos_rate_scaled[0: train_len, :]


lag_size = 50

x_train, y_train = set_lag(full_train, pos_rate_train, lag_size)
x_train = np.asarray(x_train).astype('float32')

num_features = 7

# Build and compile LSTM model
model = Sequential()
model.add(LSTM(10, return_sequences=True, input_shape=(lag_size, num_features)))
model.add(Dropout(0.5))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# Train model and track history
history = model.fit(x_train, y_train, validation_split=0.2, epochs=500, batch_size=20, verbose=2)

# Plot training and validation loss over time
plt.figure(figsize=(10, 4))
plt.plot(history.history['loss'], label='Training')
plt.plot(history.history['val_loss'], label='Validation')
plt.legend()
plt.xlabel('Epoch', fontsize=14)
plt.ylabel('Mean Squared Error', fontsize=14)
plt.title('Testing Results of LSTM Model with Window Size = ' + str(lag_size), fontsize=17)
plt.show()


# Test model on full range of data
y_hat = model.predict(x_train)
y_hat = np.mean(y_hat, axis=1)
y_hat = scaler.inverse_transform(y_hat)
y_train = scaler.inverse_transform(y_train.reshape(len(y_train), 1))

# Plot the model's prediction
fig, ax = plt.subplots(figsize=(8, 4))

# Separate plots for training and validation data
valid_ind = round(len(x_train) * 0.8)
trimmed_dates = comp_df['day'][lag_size + 1:]

ax.plot(trimmed_dates[:valid_ind], y_hat[:valid_ind, :], label='Training')
ax.plot(trimmed_dates[valid_ind:], y_hat[valid_ind:, :], label='Testing')
ax.plot(trimmed_dates, y_train, label='Real Data')
ax.legend()

plt.show()
fig.savefig('demo.png', transparent=True)

