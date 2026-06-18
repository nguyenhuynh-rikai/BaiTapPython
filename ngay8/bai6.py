from shapely.geometry import Point, Polygon
import geopandas as gpd
import matplotlib.pyplot as plt
poly = Polygon([
    (108.15, 16.00),
    (108.25, 16.00),
    (108.25, 16.10),
    (108.15, 16.10)
])

point = Point(108.20, 16.05)

gdf_poly = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")
gdf_point = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")

ax = gdf_poly.plot(edgecolor="red")
gdf_point.plot(ax=ax, color= "blue")
plt.show()
print(point.within(poly))