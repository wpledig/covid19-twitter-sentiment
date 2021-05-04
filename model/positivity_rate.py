from statsmodels.tsa.stattools import adfuller
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from numpy import log
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

#Read in the datasets, in this case the vader results and positivity rates to keep things simple
pd.set_option('mode.chained_assignment', None)
us_data = pd.read_csv("data/positivty_rate.csv")
vader_data = pd.read_csv("data/vader_compound_dailies.csv")
covid_df = us_data["pos_rate"]
vader_df = vader_data["average_compound"]

# We are limited by the tweets we have in terms of training data, so we need to extract only the data that corresponds
# to days that both datasets have data for
#vader training data is from 7-26 to 1-25
training_indices = range(0,183)
testing_indices = range(183, 214)

# The magic numbers below are the indidices in the dataframes where we want to start and stop pulling data from,
# basically only look at the relevant data between the dates given at those indices
# Sets the indices of each help with plotting later
actual_df = covid_df.iloc[330:361]
actual_df.index = testing_indices
training_df = covid_df.iloc[147:330]
training_df.index = training_indices
exog_df = vader_df.iloc[183:214]
exog_df = exog_df.reset_index(drop=True)
vader_df = vader_df.iloc[:183]

# Actually make the model with the data extracted above, filling in the training data, training_df, and exogenous variable, vader_df,
# alongside the optimal hyperparameters gotten from arima.py. These hyperparams are different from (0, 2, 0) b/c we changed from the NYTimes
# COVID-19 data to COVID-19 positivity rate data
model = ARIMA(training_df, exog = vader_df, order=(2, 1, 0))
results = model.fit()

# Use the model to predict the next month's worth of positivity rates, using the rest of the vader_df as the exog var to feed in
forecast_model = results.predict(start= 183, end = 213, exog = exog_df)

# Make as pandas series to help graph
fc_series = pd.Series(forecast_model, index=actual_df.index)
#lower_series = pd.Series(conf[:, 0], index=actual_df.index)
#upper_series = pd.Series(conf[:, 1], index=actual_df.index)

# Plot
plt.plot(training_df, label='training')
plt.plot(actual_df, label='actual')
plt.plot(fc_series, label='forecast')
#plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()

# Calc and display the MSE
mse = np.square(np.subtract(actual_df, fc_series)).mean()
print(mse)

#calced MSE: 0.0019223375181610445
