import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
import os
import sys

sys.path.append(os.path.abspath("../lib"))
import modeling_utilities


# Load datasets
comp_df = modeling_utilities.get_sentiment()
emo_df = modeling_utilities.get_emotion()
pos_df = modeling_utilities.get_positivity_rate()
day_of_week = modeling_utilities.get_day_of_week()

# Scale data points to range from 0 to 1
comp_scaled, comp_scaler = modeling_utilities.scale_dataset(comp_df['average_compound'].to_numpy())
emo_scaled, emo_scaler = modeling_utilities.scale_dataset(emo_df.to_numpy()[:, 1:])
pos_rate_scaled, pos_scaler = modeling_utilities.scale_dataset(pos_df['pos_rate'].to_numpy())

# Concatenate all feature sets to one numpy array
full_scaled = np.concatenate((comp_scaled, emo_scaled, day_of_week), axis=1)

# Set the sliding window on the data
lag_size = 50
x_train, y_train = modeling_utilities.set_lag(full_scaled, pos_rate_scaled, lag_size)
x_train = np.asarray(x_train).astype('float32')

# Build and compile LSTM model
model = Sequential()
model.add(LSTM(10, return_sequences=True, input_shape=(lag_size, x_train.shape[2])))
model.add(Dropout(0.5))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# Train model and track history
history = model.fit(x_train, y_train, validation_split=0.2, epochs=300, batch_size=20, verbose=2)

# Plot training and validation loss over time
modeling_utilities.plot_loss(history.history, 'loss', 'val_loss', 'Testing Results of LSTM Model')

# Test model on full range of data
y_hat = model.predict(x_train)
y_hat = np.mean(y_hat, axis=1)
y_hat = pos_scaler.inverse_transform(y_hat)
y_train = pos_scaler.inverse_transform(y_train.reshape(len(y_train), 1))


# Plot the model's prediction
train_ind = round(len(x_train) * 0.8)
trimmed_dates = comp_df['day'][lag_size + 1:]

modeling_utilities.plot_prediction(trimmed_dates, y_train, y_hat, train_ind,
                                   'Prediction of COVID-19 Positivity Rate with LSTM Model')
