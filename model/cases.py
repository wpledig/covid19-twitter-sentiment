from statsmodels.tsa.stattools import adfuller
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from numpy import log
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt


pd.set_option('mode.chained_assignment', None)
us_data = pd.read_csv("data/us.csv")
vader_data = pd.read_csv("data/vader_compound_dailies.csv")
#covid_df = us_data["cases"][187:311].dropna()
#vader_df = vader_data["average_compound"].[0:124].dropna()

covid_df = us_data["cases"]
vader_df = vader_data["average_compound"]

actual_df = covid_df.iloc[311:341]
actual_df.index = range(124,154)
training_df = covid_df.iloc[187:311]
training_df = training_df.reset_index(drop=True)
#test_df = test_df.reset_index(drop=True)
exog_df = vader_df.iloc[183:215]
exog_df = exog_df.reset_index(drop=True)
vader_df = vader_df.iloc[:124]

#us_df.info()
#vader_df.info()

#print(vader_df)
#print(covid_df)
model = ARIMA(training_df, exog = vader_df, order=(0, 2, 0))
results = model.fit()
#results.summary()
#print(results.summary())

forecast_model = results.predict(start= 125, end = 154, exog = exog_df)
print(exog_df)
#print("Training")
#print(training_df)
#print("Forecast")
#print(forecast_model)
#print("Actual")
#print(actual_df)
# Make as pandas series
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