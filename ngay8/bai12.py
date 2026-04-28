import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

poly1 = Polygon([(0,0),(1,0),(1,1),(0,1)])
poly2 = Polygon([(1,0),(2,0),(2,1),(1,1)])
poly3 = Polygon([(0,1),(1,1),(1,2),(0,2)])

data = gpd.GeoDataFrame({
    "region": ["A", "B", "C"],
    "value": [10, 50, 100],
    "geometry": [poly1, poly2, poly3]
})

data.plot(column="value", cmap="OrRd", legend=True,edgecolor="black")

plt.show()
