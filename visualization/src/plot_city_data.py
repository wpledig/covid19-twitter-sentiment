import pandas as pd
from matplotlib.colors import Normalize
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

"""
Plots tweets per city
"""

input_file = "../../exploration/data/location_data.csv"

# initialize pandas dataframes for visualization
df = pd.read_csv(input_file)
df = df[df["lat"] != 0.0]
cities = df[df["place_type"] == 'city']
cities = cities[:2500]

# initialize matplotlib basemap
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49, projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# load the shapefile, use the name 'states'
m.readshapefile('st99_d00', name='states', drawbounds=True)

# normalize distribution of volume of tweets per city
vmin = cities["count"].min()
vmax = cities["count"].max()
norm = Normalize(vmin=vmin, vmax=vmax)

# convert geographic data to Cartesian coordinates
x, y = m(cities["lng"], cities["lat"])

m.scatter(x, y, s=cities["count"] / 50.0,  alpha=0.5)

plt.title('Number of Tweets about COVID-19 per US City')
plt.savefig('../plots/city_counts.png')
plt.show()
