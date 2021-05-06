
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from itertools import chain
import numpy as np
from sklearn.metrics import mean_squared_error
from fireTS.models import NARX
from sklearn.preprocessing import MinMaxScaler


data_range = chain(range(1, 148), range(363, 420))
stemmed_senti = pd.read_csv("../sentiment-tagging/data/vader_compound_dailies.csv", usecols=["average_compound"])
covid_data = pd.read_csv("../exploration/data/positivty_rate.csv", skiprows=data_range, usecols=['pos_rate'])


rando = np.zeros(stemmed_senti.shape)
print(rando)

x_train, x_test, y_train, y_test = train_test_split(rando, covid_data, test_size=0.20, random_state=None,
                                                    shuffle=False)

narx_mdl = NARX(LinearRegression(), auto_order=2, exog_order=[2], exog_delay=[1])
narx_mdl.fit(x_train, y_train)


# real_mse = narx_mdl.score(x_test, y_test.to_numpy().reshape((len(y_test), )), method='mse')
# print(real_mse)

ypred_narx = narx_mdl.predict(x_test, y_test, step=3)
ypred_narx = pd.Series(ypred_narx, index=y_test.index)

ypred_narx = ypred_narx[11:]
y_test = y_test[11:]

full_pred = narx_mdl.predict(rando, covid_data, step=3)
print(full_pred)
print(covid_data)

plt.plot(full_pred, label='pred')
plt.plot(covid_data, label='real')
plt.legend()
plt.show()

#print(ypred_narx)
#print(y_test)


y_test.plot(label='actual')
ypred_narx.plot(label='6-step-ahead prediction')
plt.legend()
plt.show()

mse = mean_squared_error(y_test, ypred_narx)
print(mse) 

