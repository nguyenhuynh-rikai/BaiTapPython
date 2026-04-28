import geopandas as gpd
from shapely.geometry import Point

point = Point(108.2022, 16.0544)
gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")

gdf = gdf.to_crs(epsg=3857)

gdf["geometry"] = gdf.buffer(1000)

gdf = gdf.to_crs(epsg=4326)

print(gdf)