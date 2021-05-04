# arima.py was for calculating the optimal hyperparameters of a given dataset, though it doesn't take into account exogenous variables


from statsmodels.tsa.stattools import adfuller
import pmdarima as pm
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
from numpy import log
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})

pd.set_option('mode.chained_assignment', None)
us_data = pd.read_csv("data/us.csv", header=0)
vader_data = pd.read_csv("data/vader_compound_dailies.csv", header=0)

# Start NYTimes COVID data from 7-26-2020 to 11-26-2020 to fit twitter data
covid_df = us_data.cases[187:311].dropna()
print(df)
# Adfuller
result = adfuller(df)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

# 1,1,2 ARIMA Model
#model = ARIMA(df, order=(1,1,2))
#model_fit = model.fit()
#print(model_fit.summary())

# Original Series
#fig, axes = plt.subplots(3, 2, sharex=False)
#axes[0, 0].plot(df); axes[0, 0].set_title('Original Series')
#plot_acf(df, ax=axes[0, 1])

# 1st Differencing
#axes[1, 0].plot(df.diff()); axes[1, 0].set_title('1st Order Differencing')
#plot_acf(df.diff().dropna(), ax=axes[1, 1])

# 2nd Differencing
#axes[2, 0].plot(df.diff().diff()); axes[2, 0].set_title('2nd Order Differencing')
#plot_acf(df.diff().diff().dropna(), ax=axes[2, 1])

#plt.show()


#Use the auto calculation of the hyper parameters, feeding it the dataset in place of df
model = pm.auto_arima(df, start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0,
                      D=0,
                      trace=True,
                      error_action='ignore',
                      suppress_warnings=True,
                      stepwise=True)

print(model.summary())
