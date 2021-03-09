import matplotlib.pyplot as plt
import pandas as pd
import wordcloud

"""
Creates wordcloud
"""

terms_folder = "../data-collection/data/all_term_counts_clean.csv"
df = pd.read_csv(terms_folder)

freq_dict = df.set_index('term')['counts'].to_dict()
print(freq_dict)

wordcloud = wordcloud.WordCloud(width=3200, height=1800,
                      background_color='white', max_words=1000,
                      min_font_size=10).generate_from_frequencies(freq_dict)

# plot the WordCloud image
plt.figure(figsize=(32, 18), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()