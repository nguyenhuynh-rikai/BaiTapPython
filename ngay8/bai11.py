import geopandas as gpd

gdf = gpd.read_file("data/gadm41_VNM_1.shp")

gdf = gdf.to_crs(epsg=32648)

gdf["area_m2"] = gdf.area

gdf["area_km2"] = gdf["area_m2"] / 1_000_000

print(gdf[["NAME_1", "area_km2"]].head())