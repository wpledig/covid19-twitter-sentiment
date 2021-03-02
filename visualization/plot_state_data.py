import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.image import AxesImage
from matplotlib.colorbar import ColorbarBase
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

input_file = "../exploration/location_data.csv"

df = pd.read_csv(input_file)
df = df[df["lat"] != 0.0]
cities = df[df["place_type"] == 'city']
states = df[df["place_type"] == 'admin']

m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49, projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# load the shapefile, use the name 'states'
m.readshapefile('st99_d00', name='states', drawbounds=True)

cmap = plt.cm.hot_r
vmin = states["count"].min()
vmax = states["count"].max()
norm = Normalize(vmin=vmin, vmax=vmax)

state_names = []
color_list = []
for shape_dict in m.states_info:
    cur_name = shape_dict['NAME']
    state_names.append(cur_name)
    # Don't have data for PR, so skip
    if cur_name == 'Puerto Rico':
        color_list.append([0, 0, 0, 0])
        continue
    state_count = states[states["name"] == cur_name]["count"]
    cur_color = cmap(norm(state_count))[0]
    color_list.append(cur_color)

ax = plt.gca()

for nshape, seg in enumerate(m.states):
    color = rgb2hex(color_list[nshape])
    poly = Polygon(seg, facecolor=color, edgecolor=color)
    ax.add_patch(poly)

plt.title('Number of Tweets about COVID-19 per State')
# heatmap = plt.pcolor(states["count"])

img = AxesImage(states["count"], cmap, norm=norm)
plt.colorbar(img)

plt.show()

