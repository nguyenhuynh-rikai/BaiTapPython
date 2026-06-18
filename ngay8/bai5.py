import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("data/gadm41_VNM_3.shp")

print(gdf.head())

gdf.plot(
    edgecolor="black",
    linewidth=0.3,
    figsize=(10, 10)
)

plt.show()