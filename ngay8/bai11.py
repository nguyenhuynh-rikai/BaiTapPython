from shapely.geometry import Polygon
import geopandas as gpd

poly = Polygon([
    (108.15, 16.00),
    (108.25, 16.00),
    (108.25, 16.10),
    (108.15, 16.10)
])

gdf = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")

gdf_utm = gdf.to_crs(epsg=32648)


gdf_utm["area_m2"] = gdf_utm.area

print(gdf_utm["area_m2"])