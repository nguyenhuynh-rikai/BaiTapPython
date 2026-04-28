import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

gdf = gpd.read_file("data/gadm41_VNM_1.shp")

data = pd.DataFrame({
    "NAME_1": ["Đà Nẵng", "Hà Nội"],
    "population": [1200000, 8000000]
})

gdf = gdf.merge(data, on="NAME_1", how="left")

gdf.plot(column="population", cmap="OrRd", legend=True)

plt.title("Population by Province")
plt.show()