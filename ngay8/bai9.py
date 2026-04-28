import geopandas
from shapely.geometry import Polygon, LineString, Point
s = geopandas.GeoSeries(
    [
        Polygon([(0, 0), (1, 1), (0, 1)]),
        LineString([(0, 0), (1, 1), (1, 0)]),
        Point(0, 0),
    ]
)
print(s.centroid)
