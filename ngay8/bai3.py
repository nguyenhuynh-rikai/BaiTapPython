import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("data/my_map.shp")
# gdf = gpd.read_file("data/test.geojson")


print(gdf)

gdf.plot()
plt.show()