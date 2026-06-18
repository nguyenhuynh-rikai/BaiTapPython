import geopandas as gpd
from shapely.geometry import Point

gdf = gpd.read_file("data/gadm41_VNM_3.shp")

sindex = gdf.sindex

point = Point(108.2, 16.05)

possible_index = list(sindex.intersection(point.bounds))

print(gdf.iloc[possible_index])