
from shapely.geometry import Point
import geopandas as gpd

gdf = gpd.GeoDataFrame(
    geometry=[
        Point(108.2022, 16.0544),  # Đà Nẵng
        Point(105.8342, 21.0278)   # Hà Nội
    ],
    crs="EPSG:4326"
)

gdf = gdf.to_crs(epsg=3857)
print(len(gdf))
distance = gdf.geometry.iloc[0].distance(gdf.geometry.iloc[1])

print(distance / 1000, "km")