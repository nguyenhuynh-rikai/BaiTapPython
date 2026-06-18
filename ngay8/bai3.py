import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("data/gadm41_VNM_3.shp")
# gdf = gpd.read_file("data/test.geojson")


print(gdf)

gdf.plot()
plt.show()