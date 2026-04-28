import geopandas

from shapely.geometry import Point, LineString, Polygon
s = geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])

print(s)

line = geopandas.GeoSeries(LineString([(1, 1), (2, 2), (3, 3)]))

print(line)

polygon = geopandas.GeoSeries(Polygon([(1, 1), (2, 2), (3, 3)]))

print(polygon)