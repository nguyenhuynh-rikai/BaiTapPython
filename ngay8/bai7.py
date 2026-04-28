from shapely.geometry import Point, Polygon
import geopandas as gpd
import matplotlib.pyplot as plt

poly1 = Polygon([
    (108.15, 16.00),
    (108.20, 16.00),
    (108.20, 16.05),
    (108.15, 16.05)
])

poly2 = Polygon([
    (108.20, 16.00),
    (108.25, 16.00),
    (108.25, 16.05),
    (108.20, 16.05)
])

gdf_poly = gpd.GeoDataFrame(
    {"area": ["A", "B"], "geometry": [poly1, poly2]},
    crs="EPSG:4326"
)


points = [
    Point(108.17, 16.02),
    Point(108.22, 16.02),
    Point(108.30, 16.10)
]

gdf_point = gpd.GeoDataFrame(
    {"user": ["U1", "U2", "U3"], "geometry": points},
    crs="EPSG:4326"
)


ax = gdf_poly.plot(edgecolor="black")
gdf_point.plot(ax=ax, color="red")

result = gpd.sjoin(gdf_point, gdf_poly, how="left", predicate="within")
plt.show()
print(result)