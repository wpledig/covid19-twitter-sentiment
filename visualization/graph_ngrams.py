import matplotlib.pyplot as plt
import pandas as pd

"""
Graphs the three n-grams plots
"""


def make_bar(df, key, end):
    """
    Creates a horizontal bar plot formatted for an input set of n-grams counts.

    :param df: a Dataframe containing columns 'counts' and key
    :param key: the column of df containing the n-grams as a string
    :param end: the number of n-grams
    :return: Nothing.
    """
    # Selecting data to be plotted
    df = df[:end]
    plt.figure(figsize=(10, 7))
    plt.barh(range(df.shape[0]), df['counts'])
    plt.ticklabel_format(style='plain')
    
    plt.yticks(range(df.shape[0]), df[key])
    plt.gca().invert_yaxis()
    
    # Creating labels/titles.
    plt.xlabel('Number of Appearances')
    plt.title('25 Most Common Terms in Covid-Related Tweets')
    plt.show()


# Creating variables for csv files
terms_folder = "../data-collection/data/all_term_counts_clean.csv"
bigrams_folder = "../data-collection/data/all_bigram_counts_clean.csv"
trigrams_folder = "../data-collection/data/all_trigram_counts_clean.csv"

# Reading in csv files.
o_df = pd.read_csv(terms_folder)
b_df = pd.read_csv(bigrams_folder)
t_df = pd.read_csv(trigrams_folder)

# Creating horizontal bar plots of previous csv files.
make_bar(o_df, 'term', 25)

make_bar(b_df, 'gram', 25)

make_bar(t_df, 'gram', 25)
