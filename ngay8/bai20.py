import folium
import geopandas as gpd
from folium.plugins import HeatMap

gdf = gpd.read_file("data/gadm41_VNM_1.shp")

m = folium.Map(location=[16.0544, 108.2022], zoom_start=6)

folium.Marker(
    location=[16.0544, 108.2022],
    popup="Da Nang",
    tooltip="Click me"
).add_to(m)

folium.GeoJson(
    gdf,
    name="Vietnam Provinces",
    tooltip=folium.GeoJsonTooltip(fields=["NAME_1"])
).add_to(m)

gdf["value"] = range(len(gdf))

folium.Choropleth(
    geo_data=gdf,
    data=gdf,
    columns=["NAME_1", "value"],
    key_on="feature.properties.NAME_1",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Demo Value"
).add_to(m)

gdf["centroid"] = gdf.geometry.centroid

heat_data = [[geom.y, geom.x] for geom in gdf["centroid"]]

HeatMap(
    heat_data,
    radius=15,
    blur=10
).add_to(m)

folium.LayerControl().add_to(m)

m.save("map.html")