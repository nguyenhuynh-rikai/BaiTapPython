from shapely.geometry import Polygon
import geopandas as gpd
import matplotlib.pyplot as plt

poly = Polygon([
    (108.15, 16.00),
    (108.25, 16.00),
    (108.25, 16.10),
    (108.15, 16.10)
])

gdf = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")

gdf["centroid"] = gdf.centroid

ax = gdf.plot(edgecolor="black")
gdf["centroid"].plot(ax=ax, color="red")

plt.show()

print(gdf["centroid"])