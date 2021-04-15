import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath("../lib"))
from plot_utilities import make_ngram_bar

"""
Graphs the three n-grams plots
"""

# Creating variables for csv files
terms_folder = "../../data-collection/data/all_term_counts_clean.csv"
bigrams_folder = "../../data-collection/data/all_bigram_counts_clean.csv"
trigrams_folder = "../../data-collection/data/all_trigram_counts_clean.csv"

# Reading in csv files.
o_df = pd.read_csv(terms_folder)
b_df = pd.read_csv(bigrams_folder)
t_df = pd.read_csv(trigrams_folder)

# Creating horizontal bar plots of previous csv files.
make_ngram_bar(o_df, 'term', 25)

make_ngram_bar(b_df, 'gram', 25)

make_ngram_bar(t_df, 'gram', 25)
