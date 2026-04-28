import folium
from folium.plugins import HeatMap

m = folium.Map(location=[16.0544, 108.2022], zoom_start=12)

data = [
    [16.05, 108.20],
    [16.06, 108.21],
    [16.07, 108.22],
    [16.05, 108.20]
]

HeatMap(data).add_to(m)

m.save("heatmap.html")