import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("data/my_map.shp")

gdf["geometry_simplified"] = gdf.geometry.simplify(0.1)

gdf.set_geometry("geometry_simplified").plot()

plt.show()