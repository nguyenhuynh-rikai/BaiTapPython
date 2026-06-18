from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geo_app")

location = geolocator.geocode("Da Nang, Vietnam")

print(location.address)
print(location.latitude, location.longitude)