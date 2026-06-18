from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="reverse_geo_app")

location = geolocator.reverse((16.0544, 108.2022))

print(location.address)