import geopandas as gpd

gdf = gpd.read_file("data/world-country-boundaries.kml", driver="KML")

# print(gdf.head())
#
# print(gdf.columns)
# print(gdf.geometry)
# print(gdf.crs)

gdf.plot()

gdf.to_file("output.kml", driver="KML")