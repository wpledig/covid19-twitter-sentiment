from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from fireTS.models import NARX
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

# Create and train NARX model
model = NARX(RandomForestRegressor(), auto_order=2, exog_order=[2], exog_delay=[1])
model.fit(x_train, y_train)

# Use the model to create a prediction and plot the results
full_prediction = model.predict(comp_scaled, pos_rate_scaled, step=3)
full_pred_rescaled = pos_scaler.inverse_transform(full_prediction.reshape(-1, 1))
modeling_utilities.plot_prediction(comp_df['day'], pos_df['pos_rate'], full_pred_rescaled, len(y_train),
                                   'Prediction of COVID-19 Positivity Rate with NARX Model')


# Print MSE for both training and testing
mse = mean_squared_error(pos_rate_scaled[5:len(y_train)], full_prediction[5:len(y_train)])
print('Training MSE =', mse)

mse = mean_squared_error(pos_rate_scaled[len(y_train):], full_prediction[len(y_train):])
print('Testing MSE =', mse)
