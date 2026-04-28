import geopandas as gpd

gdf = gpd.read_file("data/gadm41_VNM_3.shp")
gdf = gdf.to_crs("EPSG:3857")

gdf["area"] = gdf.geometry.area

print(gdf["area"])