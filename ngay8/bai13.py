import geopandas as gpd

gdf = gpd.read_file("data/gadm41_VNM_3.shp")
gdf = gdf.to_crs("EPSG:4326")

g1 = gdf.iloc[:50]
g2 = gdf.iloc[50:100]

inter = gpd.overlay(g1, g2, how="intersection")
union = gpd.overlay(g1, g2, how="union")

print(inter)
print(union)