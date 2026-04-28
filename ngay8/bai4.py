import geopandas as gpd

gdf = gpd.read_file("data/map.shp")
gdf = gdf.set_crs(epsg=32648)

print(gdf.crs)