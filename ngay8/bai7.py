import geopandas as gpd
from shapely.geometry import Point

gdf_provinces = gpd.read_file("data/gadm41_VNM_1.shp").to_crs(epsg=4326)

points = gpd.GeoDataFrame(
    {
        "id": [1, 2],
        "geometry": [Point(108.2022, 16.0544), Point(105.8342, 21.0278)]
    },
    crs="EPSG:4326"
)
result = gpd.sjoin(points, gdf_provinces, predicate="within")

print(result[["id", "NAME_1"]])