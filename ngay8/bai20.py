import geopandas as gpd
import folium

gdf = gpd.read_file("data/gadm41_VNM_3.shp")
gdf = gdf.to_crs("EPSG:4326")

m = folium.Map(location=[16.05, 108.2], zoom_start=6)

folium.GeoJson(
    gdf,
    tooltip=folium.GeoJsonTooltip(fields=["NAME_1", "NAME_2", "NAME_3"],
                                   aliases=["Tỉnh:", "Huyện:", "Xã:"])
).add_to(m)

m.save("interactive_map.html")
