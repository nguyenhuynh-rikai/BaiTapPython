from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt

point = Point(105.20, 16.05)

gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")

gdf_utm = gdf.to_crs(epsg=32648)
2
gdf_utm["buffer"] = gdf_utm.buffer(2000)

ax = gdf_utm.plot(color="red")
gdf_utm["buffer"].plot(ax=ax, alpha=0.3)

plt.show()