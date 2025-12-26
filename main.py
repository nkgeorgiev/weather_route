from fastapi import FastAPI, Query
from datetime import datetime

from services.geocoding import geocode_place
from services.routing import get_route
from services.sampling import sample_route_every_km
from services.weather import get_weather_for_points


from settings import settings

app = FastAPI(title="Route Weather API")


@app.get("/route-weather")
def route_weather(
    origin: str = Query(...),
    destination: str = Query(...),
    departure_time: datetime = Query(...),
):
    ors_key = settings.ORS_API_KEY
    tomorrow_key = settings.TOMORROW_API_KEY

    origin_coords = geocode_place(origin)
    destination_coords = geocode_place(destination)

    route = get_route(ors_key, origin_coords, destination_coords)

    sampled_points = sample_route_every_km(
        route["coordinates"],
        route["distance_km"],
        route["duration_seconds"],
        interval_km=50,
        departure_time=departure_time
    )

    weather = get_weather_for_points(tomorrow_key,sampled_points)

    return {
        "origin": origin,
        "destination": destination,
        "distance_km": route["distance_km"],
        "duration_hours": round(route["duration_seconds"] / 3600, 2),
        "points": weather
    }
