from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf, grangercausalitytests
import pandas as pd
import numpy as np

df1 = pd.read_csv("../sentiment-tagging/data/vader_compound_dailies.csv", parse_dates=['day'], infer_datetime_format=True)


case_df = pd.read_csv("../data-collection/data/nytimes-us.csv", parse_dates=['date'], infer_datetime_format=True)
case_df["new_cases"] = 0
for index, row in case_df.iterrows():
    if index > 1:
        case_df["new_cases"][index] = case_df["cases"][index] - case_df["cases"][index - 1]

# Trim set of cases to date range found in Tweet dataset
case_df = case_df[case_df["date"] >= df1['day'][0]]
case_df = case_df[case_df["date"] <= df1['day'][df1.shape[0] - 1]]
case_df = case_df.reset_index(drop=True)

df1['infec'] = case_df['new_cases']
df1['test'] = np.random.rand(df1.shape[0])

print(df1['test'])

res = grangercausalitytests(df1[['average_compound', 'infec']], maxlag=15)

res2 = grangercausalitytests(df1[['average_compound', 'test']], maxlag=15)