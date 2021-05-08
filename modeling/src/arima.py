from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import os
import sys

sys.path.append(os.path.abspath("../lib"))
import modeling_utilities


# Load data
comp_df = modeling_utilities.get_sentiment()
pos_df = modeling_utilities.get_positivity_rate()

# Scale data to range from 0 to 1
comp_scaled, comp_scaler = modeling_utilities.scale_dataset(comp_df['average_compound'].to_numpy())
pos_rate_scaled, pos_scaler = modeling_utilities.scale_dataset(pos_df['pos_rate'].to_numpy())

# Split data into training and testing
x_train, x_test, y_train, y_test = train_test_split(comp_scaled, pos_rate_scaled, test_size=0.20, random_state=None,
                                                    shuffle=False)

# Create and train the ARIMA model
model = ARIMA(y_train, exog=x_train, order=(2, 1, 0))
model_res = model.fit()

# Create a forecast and plot it
forecast = model_res.predict(start=len(y_train), end=len(pos_rate_scaled) - 1, exog=x_test)
modeling_utilities.plot_prediction(comp_df['day'][len(y_train):], y_test, forecast, 0,
                                   'Prediction of COVID-19 Positivity Rate with ARIMA Model')

# Print out MSE loss
mse = mean_squared_error(y_test, forecast)
print('Testing MSE =', mse)
