import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

gdf = gpd.read_file("data/gadm41_VNM_3.shp")

gdf["value"] = np.random.randint(1, 100, len(gdf))

gdf.plot(column="value", cmap="OrRd", legend=True)

plt.show()