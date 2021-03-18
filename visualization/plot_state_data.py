import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.image import AxesImage
from matplotlib.colorbar import ColorbarBase
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

"""
Plots tweets by state
"""


input_file = "../exploration/location_data.csv"
pop_file = "../data-collection/data/nst-est2020.csv"

# Load population data and calculate population by million
pop_df = pd.read_csv(pop_file)
pop_df = pop_df[["NAME", "POPESTIMATE2020"]]
pop_df["pop_by_mill"] = pop_df["POPESTIMATE2020"] / 1000000.0

# Load state counts
df = pd.read_csv(input_file)
df = df[df["lat"] != 0.0]
states = df[df["place_type"] == 'admin']
states = pd.merge(states, pop_df, left_on='name', right_on='NAME')
# Calculate tweet count by population for each state
states["count_by_pop"] = states["count"] / states["pop_by_mill"]

# Load the map for rendering
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49, projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
m.readshapefile('st99_d00', name='states', drawbounds=True)

# Set heatmap color and normalization function
cmap = plt.cm.hot_r
vmin = states["count_by_pop"].min()
vmax = states["count_by_pop"].max()
norm = Normalize(vmin=vmin, vmax=vmax)

# Calculate the color for each state in the heatmap and store in "color_list"
state_names = []
color_list = []
for shape_dict in m.states_info:
    cur_name = shape_dict['NAME']
    state_names.append(cur_name)
    # Don't have data-collection for PR, so skip
    if cur_name == 'Puerto Rico':
        color_list.append([0, 0, 0, 0])
        continue
    state_count = states[states["name"] == cur_name]["count_by_pop"]
    cur_color = cmap(norm(state_count))[0]
    color_list.append(cur_color)

ax = plt.gca()

# Color each state and render on map
for nshape, seg in enumerate(m.states):
    color = rgb2hex(color_list[nshape])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)

plt.title('Number of Tweets per Million Residents\n about COVID-19 per State')

# Render the colorbar legend
img = AxesImage(states["count_by_pop"], cmap, norm=norm)
cb = plt.colorbar(img)

print(states[["name", "count", "count_by_pop"]])

plt.savefig('state_counts_by_pop.png')
plt.show()

