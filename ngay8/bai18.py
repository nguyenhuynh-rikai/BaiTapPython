import geopandas as gpd

gdf = gpd.read_file("data/gadm41_VNM_1.shp")

sindex = gdf.sindex

geom = gdf.geometry[0]

possible_matches_index = list(sindex.intersection(geom.bounds))

possible_matches = gdf.iloc[possible_matches_index]

final = possible_matches[possible_matches.intersects(geom)]
print(final)