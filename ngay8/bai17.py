import geopandas as gpd
import matplotlib.pyplot as plt
gdf = gpd.read_file("data/gadm41_VNM_1.shp")

gdf["geometry_simple"] = gdf.geometry.simplify(tolerance=0.01)

print(gdf.head())

fig, ax = plt.subplots(1, 2)

gdf.plot(ax=ax[0])
ax[0].set_title("Original")

gdf["geometry"].simplify(0.05).plot(ax=ax[1])
ax[1].set_title("Simplified")

plt.show()