import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath("../lib"))
from plot_utilities import running_mean, plot_avgs

plt.figure(figsize=(10, 6))

stem_df = pd.read_csv("../../sentiment-tagging/data/txt2emotion_dailies.csv", parse_dates=['day'], infer_datetime_format=True)
# Adjust all emotion fields to be difference from average
stem_df['sad'] -= stem_df['sad'].mean()
stem_df['angry'] -= stem_df['angry'].mean()
stem_df['surprise'] -= stem_df['surprise'].mean()
stem_df['fear'] -= stem_df['fear'].mean()
stem_df['happy'] -= stem_df['happy'].mean()

# Plot weekly averages of all emotion fields
plot_avgs(stem_df, plt, 'sad', "Sad", False, True, False)
plot_avgs(stem_df, plt, 'angry', "Angry", False, True, False)
plot_avgs(stem_df, plt, 'surprise', "Surprise", False, True, False)
plot_avgs(stem_df, plt, 'fear', "Fear", False, True, False)
plot_avgs(stem_df, plt, 'happy', "Happy", False, True, False)

# Format Plot
plt.axhline(y=0.0, color='black')
plt.legend()
plt.title('Emotion of Tweets about COVID-19 over Time in the US', fontsize=17)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Emotion Intensity Relative to Average', fontsize=14)
plt.show()

