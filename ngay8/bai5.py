from shapely.geometry import Polygon
import geopandas as gpd
import matplotlib.pyplot as plt

poly = Polygon([
    (108.15, 16.00),
    (108.25, 16.00),
    (108.25, 16.10),
    (108.15, 16.10)
])

gdf = gpd.GeoDataFrame(
    {"name": ["Da Nang Area"], "geometry": [poly]},
    crs="EPSG:4326"
)

gdf.plot()
plt.show()