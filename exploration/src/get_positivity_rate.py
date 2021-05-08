import pandas as pd

# Read in the dataset containing COVID-19 testing results by day and location
df = pd.read_csv('../../data-collection/data/covid_testing_results.csv', parse_dates=['date'], infer_datetime_format=True)

# Group dataset values by date and test outcome, summing the total numbers
agg_df = df.groupby(by=['date', 'overall_outcome']).agg({'new_results_reported': 'sum'}).reset_index()

# Create new dataframe containing the number of positive, negative, and inconclusive tests per day
rate_df = pd.DataFrame()
rate_df['date'] = agg_df[agg_df['overall_outcome'] == 'Positive'].reset_index()['date']
rate_df['pos'] = agg_df[agg_df['overall_outcome'] == 'Positive'].reset_index()['new_results_reported']
rate_df['neg'] = agg_df[agg_df['overall_outcome'] == 'Negative'].reset_index()['new_results_reported']
rate_df['inc'] = agg_df[agg_df['overall_outcome'] == 'Inconclusive'].reset_index()['new_results_reported']

# Sum the total number of tests per day by combining the three outcomes
rate_df['total'] = rate_df['pos'] + rate_df['neg'] + rate_df['inc']

# Calculate positivity rate
rate_df['pos_rate'] = rate_df['pos'] / rate_df['total']

# Save data to CSV
rate_df.to_csv("../data/positivity_rate.csv", index=False)


