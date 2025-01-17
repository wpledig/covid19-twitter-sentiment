from github import Github
import pandas as pd
import json

"""
This file compiles daily n-gram counts into total counts
"""

# The Github Repo for the original dataset
with open('../api_keys.json') as f:
    keys = json.load(f)

g = Github(keys['github_access'])
repo = g.get_repo("thepanacealab/covid19_twitter")

terms_result = pd.DataFrame(columns=['term', 'counts'])
grams_result = pd.DataFrame(columns=['gram', 'counts'])

# Used for debugging or compiling an incomplete dataset
num_dailies = 0

# Iterate across all daily folders
contents = repo.get_contents("dailies")
for daily_folder in contents:
    if daily_folder.type == 'dir':
        sub_contents = repo.get_contents(daily_folder.path)
        for content_file in sub_contents:
            # Load terms, bigrams, and trigrams data for each day and concatenate them with a running collection of data
            if content_file.name.endswith("terms.csv"):
                terms_data = pd.read_csv(content_file.download_url, header=None, names=['term', 'counts'])
                if terms_data.shape[0] == 1001:
                    terms_result = pd.concat([terms_result, terms_data])
            if content_file.name.endswith("bigrams.csv") or content_file.name.endswith("trigrams.csv"):
                grams_data = pd.read_csv(content_file.download_url, header=0)
                if grams_data.shape[0] == 1000:
                    grams_result = pd.concat([grams_result, grams_data])

        num_dailies += 1

terms_result = terms_result.astype({'counts': 'int32'})
terms_result = terms_result.astype({'term': 'str'})

grams_result = grams_result.astype({'counts': 'int32'})
grams_result = grams_result.astype({'gram': 'str'})

agg = terms_result.groupby('term', as_index=False)[['counts']].sum()
agg = agg.sort_values(by='counts', ascending=False)
agg.to_csv("../data/all_term_counts_clean.csv", index=False)

agg2 = grams_result.groupby('gram', as_index=False)[['counts']].sum()
agg2 = agg2.sort_values(by='counts', ascending=False)
agg2.to_csv("../data/all_n_gram_counts_clean.csv", index=False)

# For some reason the "bigrams" files sometimes contain trigrams and vice-versa so we need to filter the grams
# in these files by length.
count = agg2['gram'].str.split().str.len()
trigrams = agg2[~(count == 2)]
bigrams = agg2[~(count == 3)]

bigrams.to_csv("../data/all_bigram_counts_clean.csv", index=False)
trigrams.to_csv("../data/all_trigram_counts_clean.csv", index=False)


