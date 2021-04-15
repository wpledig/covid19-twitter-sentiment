import matplotlib.pyplot as plt
import pandas as pd
import wordcloud
import os

"""
Creates wordcloud
"""

# Collect and read the twitter terms
terms_folder = os.path.join(os.path.dirname(__file__), "../../data-collection/data/all_term_counts_clean.csv")
df = pd.read_csv(terms_folder)

# Generate frequency dictionary from terms
freq_dict = df.set_index('term')['counts'].to_dict()
# print(freq_dict)
print("Generating WordCloud...")

# Generate word cloud using the frequency counts
wordcloud = wordcloud.WordCloud(width=3200, height=1800,
                      background_color='white', max_words=1000,
                      min_font_size=10).generate_from_frequencies(freq_dict)

# plot the WordCloud image
plt.figure(figsize=(32, 18), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()
