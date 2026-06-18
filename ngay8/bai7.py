import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

gdf_admin = gpd.read_file("data/gadm41_VNM_3.shp")

data = pd.DataFrame({
    "name": ["A", "B", "C"],
    "lon": [108.2, 108.3, 108.25],
    "lat": [16.05, 16.1, 16.08]
})

gdf_points = gpd.GeoDataFrame(
    data,
    geometry=[Point(xy) for xy in zip(data.lon, data.lat)],
    crs="EPSG:4326"
)

gdf_admin = gdf_admin.to_crs("EPSG:4326")

result = gpd.sjoin(
    gdf_points,
    gdf_admin,
    how="left",
    predicate="within"
)

print(result[["name", "geometry"]])

ax = gdf_admin.plot(figsize=(10, 10), edgecolor="black")
gdf_points.plot(ax=ax, color="red")
plt.show()