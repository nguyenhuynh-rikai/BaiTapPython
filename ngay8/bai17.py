import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("data/gadm41_VNM_3.shp")

gdf["simple"] = gdf.geometry.simplify(0.01)

gdf.set_geometry("simple").plot()

plt.show()