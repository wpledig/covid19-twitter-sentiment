from github import Github
import pandas as pd

g = Github("247e667a9c8eaa6104e840c357e4353ce35065ae")
repo = g.get_repo("thepanacealab/covid19_twitter")

terms_result = pd.DataFrame(columns=['term', 'counts'])
grams_result = pd.DataFrame(columns=['gram', 'counts'])

# Used for debugging or compiling an incomplete dataset
num_dailies = 0

# Iterate across all daily folders
contents = repo.get_contents("dailies")
for daily_folder in contents:
    if daily_folder.type == 'dir':
        #
        sub_contents = repo.get_contents(daily_folder.path)
        for content_file in sub_contents:
            if content_file.name.endswith("terms.csv"):
                terms_data = pd.read_csv(content_file.download_url, header=None, names=['term', 'counts'])
                if terms_data.shape[0] == 1001:
                    terms_result = pd.concat([terms_result, terms_data])
            if content_file.name.endswith("bigrams.csv") or content_file.name.endswith("trigrams.csv"):
                grams_data = pd.read_csv(content_file.download_url, header=0)
                if grams_data.shape[0] == 1000:
                    grams_result = pd.concat([grams_result, grams_data])

        # print(num_dailies, daily_folder.name)
        num_dailies += 1
        # 42 -> 43
        # if num_dailies >= 43:
        #     break

terms_result = terms_result.astype({'counts': 'int32'})
terms_result = terms_result.astype({'term': 'str'})

grams_result = grams_result.astype({'counts': 'int32'})
grams_result = grams_result.astype({'gram': 'str'})

agg = terms_result.groupby('term', as_index=False)[['counts']].sum()
agg = agg.sort_values(by='counts', ascending=False)
agg.to_csv("all_term_counts_clean.csv", index=False)

agg2 = grams_result.groupby('gram', as_index=False)[['counts']].sum()
agg2 = agg2.sort_values(by='counts', ascending=False)
agg2.to_csv("all_n_gram_counts_clean.csv",index=False)

count = agg2['gram'].str.split().str.len()

trigrams = agg2[~(count == 2)]
bigrams = agg2[~(count == 3)]

bigrams.to_csv("all_bigram_counts_clean.csv", index=False)
trigrams.to_csv("all_trigram_counts_clean.csv", index=False)


