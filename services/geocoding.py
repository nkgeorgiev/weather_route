from geopy.geocoders import Nominatim
from services.http_utils import safe_request

geolocator = Nominatim(user_agent="route-weather-app")


def geocode_place(place: str):
    location = geolocator.geocode(place, featuretype="city")
    if not location:
        raise ValueError(f"Could not geocode {place}")
    
    return (location.longitude, location.latitude)