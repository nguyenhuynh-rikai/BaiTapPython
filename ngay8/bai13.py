import geopandas
from shapely.geometry import Polygon, LineString, Point
s = geopandas.GeoSeries(
    [
        Polygon([(0, 0), (2, 2), (0, 2)]),
        Polygon([(0, 0), (2, 2), (0, 2)]),
        LineString([(0, 0), (2, 2)]),
        LineString([(2, 0), (0, 2)]),
        Point(0, 1),
    ],
)
s2 = geopandas.GeoSeries(
    [
        Polygon([(0, 0), (1, 1), (0, 1)]),
        LineString([(1, 0), (1, 3)]),
        LineString([(2, 0), (0, 2)]),
        Point(1, 1),
        Point(0, 1),
    ],
    index=range(1, 6),
)

print(s.intersection(Polygon([(0, 0), (1, 1), (0, 1)])))

print(s.union(Polygon([(0, 0), (1, 1), (0, 1)])))