import geopandas as gpd
from shapely.geometry import Point

gdf = gpd.read_file("data/gadm41_VNM_3.shp")
gdf = gdf.to_crs("EPSG:3857")

p1 = Point(108.2022, 16.0544)
p2 = Point(105.8342, 21.0278)

p1 = gpd.GeoSeries([p1], crs="EPSG:4326").to_crs("EPSG:3857")[0]
p2 = gpd.GeoSeries([p2], crs="EPSG:4326").to_crs("EPSG:3857")[0]

print(p1.distance(p2))