import geopandas as gpd

gdf = gpd.read_file("C:/Nguyên/BaiTapPython/data/test.kml", driver="KML")

print(gdf.head())