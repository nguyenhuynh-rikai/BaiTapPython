import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("data/map.shp")

gdf.plot()
plt.show()