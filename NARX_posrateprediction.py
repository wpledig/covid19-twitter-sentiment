from fireTS.models import NARX, DirectAutoRegressor
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from itertools import chain
import numpy as np
from sklearn.metrics import mean_squared_error


data_range = chain(range(1, 148), range(363, 420))
stemmed_senti = pd.read_csv("/Users/justincoleman/Documents/GitHub/covid19-twitter-sentiment/sentiment-tagging/data/stemmed_daily_pos_diff.csv", usecols=["average_pos_diff"])
covid_data = pd.read_csv("/Users/justincoleman/Downloads/positivty_rate.csv", skiprows=data_range, usecols=['pos_rate'])

x_train, x_test, y_train, y_test = train_test_split(stemmed_senti, covid_data, test_size=0.20, random_state=None,
                                                    shuffle=False)

narx_mdl = NARX(LinearRegression(), auto_order=3, exog_order=[6], exog_delay=[0])
narx_mdl.fit(x_train, y_train)

ypred_narx = narx_mdl.predict(x_test, y_test, step=6)
ypred_narx = pd.Series(ypred_narx, index=y_test.index)

ypred_narx= ypred_narx[11:]
y_test=y_test[11:]

#print(ypred_narx)
#print(y_test)


y_test.plot(label='actual')
ypred_narx.plot(label='6-step-ahead prediction')
plt.legend()
plt.show()

mse = mean_squared_error(y_test, ypred_narx)
print(mse) 

