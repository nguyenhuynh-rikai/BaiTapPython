from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geo_app")

location = geolocator.reverse((16.0471, 108.2068))  # Đà Nẵng

print(location.address)