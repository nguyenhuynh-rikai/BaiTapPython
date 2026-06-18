import geopandas as gpd
import folium
from folium.plugins import HeatMap

gdf = gpd.read_file("data/gadm41_VNM_3.shp")

gdf_projected = gdf.to_crs("EPSG:3857")

centroids = gdf_projected.geometry.centroid
centroids_wgs84 = centroids.to_crs("EPSG:4326")

data = [(p.y, p.x) for p in centroids_wgs84]

# Vẽ bản đồ
m = folium.Map(location=[16.05, 108.2], zoom_start=6)

HeatMap(
    data,
    radius=15,
    blur=10,
    min_opacity=0.4
).add_to(m)

folium.LayerControl().add_to(m)
m.save("heatmap.html")
