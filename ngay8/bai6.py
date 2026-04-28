from shapely.geometry import Point
import geopandas as gpd
point = Point(108.2022, 16.0544)

gdf = gpd.read_file("data/gadm41_VNM_1.shp")

gdf = gdf.to_crs(epsg=4326)

result = gdf[gdf.contains(point)]

print(result)