from shapely.geometry import Polygon, LineString, Point
import geopandas as gpd
import matplotlib.pyplot as plt

p = Point(108, 16.55)

line = LineString([
     (198.20, 16.05),
     (108.21, 18.05)
])

poly = Polygon([
    (108.19, 16.04),
    (108.22, 16.04),
    (108.22, 16.07),
    (108.19, 16.07)
])

gs = gpd.GeoSeries([poly])
gs.plot()
plt.show()

