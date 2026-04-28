import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

poly1 = Polygon([(0,0),(2,0),(2,2),(0,2)])

poly2 = Polygon([(1,1),(3,1),(3,3),(1,3)])

gdf1 = gpd.GeoDataFrame(geometry=[poly1], crs="EPSG:4326")
gdf2 = gpd.GeoDataFrame(geometry=[poly2], crs="EPSG:4326")

# inter = gpd.overlay(gdf1, gdf2, how="intersection")
union = gpd.overlay(gdf1, gdf2, how="union")


union.plot(color="lightblue", edgecolor="black")
plt.show()
# inter.plot(edgecolor="black", color="red")
# plt.show()