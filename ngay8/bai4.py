from shapely.geometry import Point
import geopandas as gpd

points = [
    Point(108.20, 16.05),
    Point(108.21, 16.06),
]

gdf = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")

print("CRS goc:", gdf.crs)

gdf_utm = gdf.to_crs(epsg=32648)

print("CRS moi:", gdf_utm.crs)

dist = gdf_utm.distance(gdf_utm.geometry[0])

print("distance: ")
print(dist)