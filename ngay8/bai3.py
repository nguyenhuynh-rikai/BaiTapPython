import geopandas as gpd

gdf = gpd.read_file("data/map.shp")

print(gdf.head())
